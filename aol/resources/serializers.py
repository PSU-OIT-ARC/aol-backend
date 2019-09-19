import logging

from rest_framework import serializers

from . import models

logger = logging.getLogger(__name__)


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Resource
        fields = ('pk', 'name', 'url', 'rank')
