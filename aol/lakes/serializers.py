import logging

from django.template.defaultfilters import striptags, floatformat
from django.conf import settings

from rest_framework import serializers

from aol.photos.serializers import PhotoSerializer
from aol.documents.serializers import DocumentSerializer
from aol.plants.serializers import PlantObservationSerializer
from aol.mussels.serializers import MusselObservationSerializer
from aol.lakes import models

logger = logging.getLogger(__name__)


class LakeBaseSerializer(serializers.Serializer):
    title = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    county_set = serializers.SerializerMethodField()
    waterbody_type = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    shoreline = serializers.SerializerMethodField()

    def get_title(self, obj):
        return str(obj)

    def get_body(self, obj):
        text = obj.body.replace("&nbsp;", "")
        lines = striptags(text).split('\n')
        return [line for line in lines if line.strip()]

    def get_photo(self, obj):
        if not obj.photo:
            return ''

        request = self.context.get('request', None)
        if request is None:
            host = settings.ALLOWED_HOSTS[0]
            return 'https://{}/{}'.format(host, obj.photo.file.url)
        return request.build_absolute_uri(obj.photo.file.url)

    def get_county_set(self, obj):
        return ','.join([str(c) for c in obj.county_set.all()])

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
                  'title', 'body', 'photo',
                  'county_set',
                  'waterbody_type', 'area', 'shoreline', 
                  'has_mussels', 'has_plants', 'has_docs', 'has_photos')


class LakeDetailSerializer(LakeBaseSerializer, serializers.ModelSerializer):
    photos = PhotoSerializer(many=True)
    documents = DocumentSerializer(many=True)
    plants = PlantObservationSerializer(many=True, source='plant_observations')
    mussels = MusselObservationSerializer(many=True, source='mussel_observations')

    class Meta:
        model = models.Lake
        fields = ('reachcode', 'is_major',
                  'title', 'body', 'photo',
                  'county_set',
                  'waterbody_type', 'area', 'shoreline', 
                  'aol_page', 'photos', 'documents', 'plants', 'mussels')
