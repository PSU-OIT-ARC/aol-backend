import logging

from rest_framework import serializers

from . import models

logger = logging.getLogger(__name__)


class DocumentSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = models.Document
        fields = ['pk', 'type', 'name', 'file', 'rank']

    def get_file(self, obj):
        url = obj.get_absolute_url()
        return self.context['request'].build_absolute_uri(url)
