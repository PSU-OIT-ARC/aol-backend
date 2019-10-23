import logging

from rest_framework import serializers

from . import models

logger = logging.getLogger(__name__)


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Document
        fields = ('pk', 'name', 'type',
                  'file', 'friendly_filename', 'rank')
