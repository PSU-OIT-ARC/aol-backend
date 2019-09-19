from django.db import models

from aol.plants import enums


class Plant(models.Model):
    name = models.CharField(max_length=255)
    normalized_name = models.CharField(max_length=255, unique=True)
    common_name = models.CharField(max_length=255)
    noxious_weed_designation = models.CharField(max_length=255,
                                                default=enums.NOXIOUS_WEED_DESIGNATION_NONE,
                                                choices=enums.NOXIOUS_WEED_DESIGNATION_CHOICES)
    is_native = models.NullBooleanField(default=None,
                                        choices=enums.NATIVE_CHOICES)

    class Meta:
        ordering = ('normalized_name', )

    def __str__(self):
        return self.normalized_name


class PlantObservation(models.Model):
    lake = models.ForeignKey('lakes.Lake', related_name='plant_observations',
                             on_delete=models.CASCADE)
    plant = models.ForeignKey('plants.Plant', related_name="lakes",
                              on_delete=models.CASCADE)
    observation_date = models.DateField(null=True)
    source = models.CharField(max_length=255,
                              default=enums.REPORTING_SOURCE_NONE,
                              choices=enums.REPORTING_SOURCE_CHOICES)
    survey_org = models.CharField(max_length=255)

    class Meta:
        unique_together = ('lake', 'plant', 'observation_date')
        ordering = ('-observation_date', )

    def source_link(self):
        urls = dict(enums.REPORTING_SOURCE_URL)
        return urls.get(self.source, None)

    def __str__(self):
        params = (self.lake, self.plant, self.observation_date, self.survey_org)
        return '{} - {} ({}, {})'.format(*params)
