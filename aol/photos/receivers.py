from django.db.models import signals
from django.dispatch import receiver

from aol.photos.models import Photo


@receiver(signals.post_save, sender=Photo)
def review_lake_status(sender, **kwargs):
    instance = kwargs.pop('instance')
    instance.lake.update_status()
    instance.lake.save()
