from django.db import models


class ReportingAgency(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'reporting agencies'

    def __str__(self):
        return self.name


class Mussel(models.Model):
    name = models.TextField()
    machine_name = models.CharField(max_length=30)
    is_scientific_name = models.BooleanField()

    class Meta:
        verbose_name = 'mollusc specie'

    def __str__(self):
        return self.machine_name


class MusselObservation(models.Model):
    lake = models.ForeignKey('lakes.Lake', related_name='mussel_observations',
                             on_delete=models.CASCADE)
    agency = models.ForeignKey(ReportingAgency,
                               on_delete=models.CASCADE)
    specie = models.ForeignKey(Mussel,
                               on_delete=models.CASCADE)
    physical_description = models.TextField()

    date_checked = models.DateField()
    approved = models.BooleanField()

    class Meta:
        verbose_name = 'mollusc observation'

    def __str__(self):
        return '{} ({}, {})'.format(self.specie, self.agency, self.date_checked)
