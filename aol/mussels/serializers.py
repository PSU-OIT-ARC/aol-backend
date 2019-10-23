import logging

from rest_framework import serializers

from aol.mussels import models

logger = logging.getLogger(__name__)


class MusselSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = models.Mussel
        fields = ('name', 'machine_name', 'is_scientific_name')


class MusselObservationSerializer(serializers.ModelSerializer):
    mussel = MusselSerializer()

    data_provider = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = models.MusselObservation
        fields = ('mussel',
                  'date_sampled', 'target',
                  'collection_method', 'data_provider',
                  'status_display')

    def get_data_provider(self, obj):
        return obj.collecting_agency.split(',')

    def get_status_display(self, obj):
        return obj.get_status_display()
