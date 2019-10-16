from django.utils.functional import cached_property
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Area, Perimeter
from django.contrib.gis.db import models
from django.db.models import Q

from aol.lakes import enums


class County(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'counties'

    def __str__(self):
        return self.name


class FishingZone(models.Model):
    odfw = models.CharField(max_length=255)

    def __str__(self):
        return self.odfw.capitalize()

    def get_absolute_url(self):
        return "https://myodfw.com/recreation-report/fishing-report/{}-zone".format(self.odfw.lower())


class LakeManager(models.Manager):
    """
    We only want to return lakes that are coded as LakePond or Reservoir
    which have the types 390, 436 in the NHD.

    Refs: https://prd-wret.s3-us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/NHDv2.2.1_poster_081216.pdf
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(parent__isnull=True)

    def get_for_point(self, lon, lat):
        queryset = self.get_queryset()
        coord_transform = CoordTransform(SpatialReference(4326),
                                         SpatialReference(3644))
        point_geom = Point(lon, lat)
        point_geom.transform(coord_transform)
        return queryset.filter(the_geom__contains=point_geom)

    def major(self):
        queryset = self.get_queryset()
        return queryset.filter(
            is_major=True,
            waterbody_type__in=[enums.WATERBODY_TYPE_LAKE_POND,
                                enums.WATERBODY_TYPE_RESERVOIR]
        )

    def minor(self):
        queryset = self.get_queryset()
        queryset = queryset.exclude(gnis_id='')
        return queryset.filter(
            is_major=False,
            waterbody_type__in=[enums.WATERBODY_TYPE_LAKE_POND,
                                enums.WATERBODY_TYPE_RESERVOIR]
        )


class Lake(models.Model):
    title = models.CharField(max_length=255, blank=True)
    aol_page = models.IntegerField(null=True, blank=True)
    body = models.TextField()
    photo = models.ForeignKey('photos.Photo', null=True,
                              related_name='lake_cover_photo',
                              on_delete=models.SET_NULL)

    reachcode = models.CharField(max_length=32, primary_key=True)
    permanent_id = models.CharField(max_length=64)
    parent = models.ForeignKey('self', null=True, blank=True,
                               on_delete=models.SET_NULL)

    gnis_id = models.CharField(max_length=32)
    gnis_name = models.CharField(max_length=255)

    fishing_zone = models.ForeignKey('FishingZone', null=True,
                                     on_delete=models.SET_NULL)
    county_set = models.ManyToManyField('County')
    plants = models.ManyToManyField('plants.Plant', through="plants.PlantObservation")
    mussels = models.ManyToManyField('mussels.Mussel', through="mussels.MusselObservation")

    the_geom = models.MultiPolygonField('Lake geometry', srid=3644)
    waterbody_type = models.IntegerField(choices=enums.WATERBODY_TYPE_CHOICES,
                                         default=enums.WATERBODY_TYPE_UNKNOWN)

    is_major = models.BooleanField(default=False, db_index=True)
    has_photos = models.BooleanField(default=False, db_index=True)
    has_docs = models.BooleanField(default=False, db_index=True)
    has_resources = models.BooleanField(default=False, db_index=True)
    has_plants = models.BooleanField(default=False, db_index=True)
    has_mussels = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ('is_major', 'title', )

    @property
    def counties(self):
        """
        Return a nice comma separated list of the counties this lake belongs to
        """
        if not hasattr(self, "_counties"):
            self._counties = ", ".join(c.name for c in self.county_set.all())
        return self._counties

    @counties.setter
    def counties(self, value):
        """
        We need a setter since the raw query we perform in the manager class
        generates the comma separated list of counties in the query itself
        """
        self._counties = value

    @property
    def area(self):
        obj = Lake.objects.filter(pk=self.pk).annotate(computed_area=Area('the_geom')).get()
        # area is given in sq ft.; however, GeoDjango believes it to be sq m.
        return obj.computed_area.standard / 43560.04

    @property
    def shoreline(self):
        obj = Lake.objects.filter(pk=self.pk).annotate(computed_shoreline=Perimeter('the_geom')).get()
        return obj.computed_shoreline.mi

    def update_status(self):
        """
        TBD
        """
        self._status_updated = True

        self.has_photos = self.photos.exists()
        self.has_docs = self.documents.exists()
        self.has_resources = self.resources.exists()
        self.has_plants = self.plant_observations.exists()
        self.has_mussels = self.mussel_observations.exists()

        self.is_major = False
        if any([self.aol_page is not None,
                self.has_photos,
                self.has_docs,
                self.has_resources,
                self.has_plants,
                self.has_mussels]):
            self.is_major = True

    def __str__(self):
        return self.title or self.gnis_name

    objects = models.Manager()
    active = LakeManager()
