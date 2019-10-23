import tempfile

from django.core.management import call_command
from django.db import models

from aol.mussels import enums


class Mussel(models.Model):
    name = models.TextField()
    machine_name = models.CharField(max_length=30)
    is_scientific_name = models.BooleanField()

    class Meta:
        verbose_name = 'mollusc'
        ordering = ('machine_name',)

    def __str__(self):
        return self.machine_name


class MusselObservation(models.Model):
    lake = models.ForeignKey('lakes.Lake', related_name='mussel_observations',
                             on_delete=models.CASCADE)
    mussel = models.ForeignKey(Mussel, null=True, on_delete=models.CASCADE)

    date_sampled = models.DateField()
    target = models.CharField(max_length=32)
    collection_method = models.CharField(max_length=64)
    collecting_agency = models.CharField(max_length=128)
    status = models.PositiveSmallIntegerField(choices=enums.STATUS_CHOICES,
                                              default=enums.STATUS_NON_DETECT)

    class Meta:
        verbose_name = 'mollusc observation'
        unique_together = ('lake', 'mussel', 'date_sampled', 'target')
        ordering = ('-date_sampled', )

    def __str__(self):
        if self.mussel is not None:
            params = (self.lake, self.mussel, self.date_sampled, self.collecting_agency)
            return '{} - {} ({}, {})'.format(*params)

        params = (self.lake, self.date_sampled, self.collecting_agency)
        return '{} ({}, {})'.format(*params)


class ImportedMusselObservation(models.Model):
    status = models.PositiveSmallIntegerField(choices=enums.IMPORT_STATUS_CHOICES,
                                              default=enums.IMPORT_STATUS_INITIALIZED)
    datafile = models.FileField()
    output = models.TextField()

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'imported mollusc datafile'
        ordering = ('-created_on', '-updated_on')

    def __str__(self):
        return '{} ({})'.format(self.datafile, self.created_on)
