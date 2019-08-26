from django.db.models import signals
from django.dispatch import receiver

from aol.plants.models import PlantObservation


@receiver(signals.post_save, sender=PlantObservation)
def review_lake_status(sender, **kwargs):
    instance = kwargs.pop('instance')
    instance.lake.update_status()
    instance.lake.save()
