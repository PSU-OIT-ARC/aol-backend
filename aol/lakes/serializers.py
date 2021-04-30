import logging
import urllib
import html
import bs4

from django.template.defaultfilters import (striptags, floatformat,
                                            truncatechars)
from django.contrib.sites.models import Site
from django.conf import settings

from rest_framework import serializers

from aol.photos.serializers import PhotoSerializer
from aol.documents.serializers import DocumentSerializer
from aol.resources.serializers import ResourceSerializer
from aol.plants.serializers import PlantObservationSerializer
from aol.mussels.serializers import MusselObservationSerializer
from aol.lakes import models

logger = logging.getLogger(__name__)
site = Site.objects.get_current()


class LakeBaseSerializer(serializers.Serializer):
    title = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    counties = serializers.SerializerMethodField()
    waterbody_type = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    shoreline = serializers.SerializerMethodField()

    def get_title(self, obj):
        return str(obj)

    def get_summary(self, obj):
        parser = bs4.BeautifulSoup(obj.body, 'html.parser')
        paragraphs = parser.find_all('p')
        text = ''

        if not paragraphs:
            text = obj.body
        else:
            for p in paragraphs:
                if striptags(p).strip():
                    text = p
                    break

        return truncatechars(html.unescape(striptags(text)).strip(), 2000)

    def get_body(self, obj):
        # TODO: sanitize?
        return obj.body

    def get_photo(self, obj):
        if not obj.photo:
            return ''

        return urllib.parse.urljoin(
            '//{}'.format(site.domain),
            obj.photo.get_absolute_url()
        )

    def get_counties(self, obj):
        return [str(c) for c in obj.county_set.all()]

    def get_area(self, obj):
        return floatformat(obj.area, 2)

    def get_shoreline(self, obj):
        return floatformat(obj.shoreline, 2)

    def get_waterbody_type(self, obj):
        return obj.get_waterbody_type_display()


class LakeIndexSerializer(LakeBaseSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.Lake
        fields = ('reachcode', 'is_major',
                  'title', 'summary', 'photo',
                  'counties',
                  'waterbody_type', 'area', 'shoreline', 
                  'has_mussels', 'has_plants',
                  'has_photos', 'has_docs', 'has_resources')


class LakeDetailSerializer(LakeBaseSerializer, serializers.ModelSerializer):
    photos = PhotoSerializer(many=True)
    documents = DocumentSerializer(many=True)
    resources = ResourceSerializer(many=True)
    plants = PlantObservationSerializer(many=True, source='plant_observations')
    mussels = MusselObservationSerializer(many=True, source='mussel_observations')

    class Meta:
        model = models.Lake
        fields = ('reachcode', 'is_major',
                  'title', 'body', 'photo',
                  'counties',
                  'waterbody_type', 'area', 'shoreline', 
                  'aol_page',
                  'photos', 'documents', 'resources',
                  'plants', 'mussels')
