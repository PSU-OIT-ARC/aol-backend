import logging

from rest_framework import serializers

from django.contrib.flatpages import models

logger = logging.getLogger(__name__)


class FlatPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FlatPage
        fields = ('url', 'title', 'content')
