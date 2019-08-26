from django.db.models import signals
from django.dispatch import receiver

from aol.lakes.models import Lake


@receiver(signals.pre_save, sender=Lake)
def review_lake_status(sender, **kwargs):
    instance = kwargs.pop('instance')
    if not hasattr(instance, '_status_updated'):
        instance.update_status()
