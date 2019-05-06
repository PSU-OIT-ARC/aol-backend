from django.db.models import signals
from django.dispatch import receiver

from aol.documents.models import Document


@receiver(signals.post_save, sender=Document)
def review_lake_status(sender, **kwargs):
    instance = kwargs.pop('instance')
    instance.lake.update_status()
    instance.lake.save()
