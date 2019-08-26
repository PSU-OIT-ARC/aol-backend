import logging

from rest_framework import serializers

from aol.mussels import models

logger = logging.getLogger(__name__)


class MusselSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = models.Mussel
        fields = ('name', )


class MusselObservationSerializer(serializers.ModelSerializer):
    specie = MusselSerializer()
    agency = serializers.CharField()
    date_checked = serializers.DateField()

    class Meta:
        model = models.MusselObservation
        fields = ('specie', 'agency', 'date_checked')
