import logging

from rest_framework import serializers

from aol.plants import models

logger = logging.getLogger(__name__)


class PlantSerializer(serializers.ModelSerializer):
    noxious_weed_designation = serializers.SerializerMethodField()

    class Meta:
        model = models.Plant
        fields = ('name',
                  'normalized_name', 'common_name',
                  'noxious_weed_designation', 'is_native')

    def get_noxious_weed_designation(self, obj):
        return obj.get_noxious_weed_designation_display()


class PlantObservationSerializer(serializers.ModelSerializer):
    plant = PlantSerializer()
    source_display = serializers.SerializerMethodField()
    
    class Meta:
        model = models.PlantObservation
        fields = ('plant',
                  'observation_date', 'source_display', 'survey_org')

    def get_source_display(self, obj):
        return obj.get_source_display()


