from django.db.models import signals
from django.dispatch import receiver

from aol.resources.models import Resource


@receiver(signals.post_save, sender=Resource)
@receiver(signals.pre_delete, sender=Resource)
def review_lake_status(sender, **kwargs):
    instance = kwargs.pop('instance')
    instance.lake.update_status()
    instance.lake.save()
