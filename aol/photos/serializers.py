import logging

from rest_framework import serializers

from . import models

logger = logging.getLogger(__name__)


class PhotoSerializer(serializers.ModelSerializer):
    href = serializers.FileField(source='file')
    description = serializers.CharField(source='caption')

    class Meta:
        model = models.Photo
        fields = ('pk', 'href',
                  'author', 'description', 'taken_on')
