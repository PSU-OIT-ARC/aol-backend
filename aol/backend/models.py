from django.core.cache import caches
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save)
def invalidate_cache(sender, **kwargs):
    caches['default'].clear()
