from django.db.models import signals
from django.dispatch import receiver

from aol.mussels.models import MusselObservation


@receiver(signals.post_save, sender=MusselObservation)
@receiver(signals.pre_delete, sender=MusselObservation)
def review_lake_status(sender, **kwargs):
    instance = kwargs.pop('instance')
    instance.lake.update_status()
    instance.lake.save()
