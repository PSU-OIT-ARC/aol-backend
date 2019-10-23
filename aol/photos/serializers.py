import logging

from rest_framework import serializers

from django.template.defaultfilters import truncatechars

from . import models

logger = logging.getLogger(__name__)


class PhotoSerializer(serializers.ModelSerializer):
    href = serializers.FileField(source='file')
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = models.Photo
        fields = ('pk', 'href',
                  'title', 'description')

    def get_title(self, obj):
        return truncatechars(obj.caption, 30)

    def get_description(self, obj):
        elements = [obj.author or "Unknown"]
        if obj.taken_on is not None:
            elements.append(' - Taken on {}'.format(obj.taken_on))
        return ''.join(elements)
