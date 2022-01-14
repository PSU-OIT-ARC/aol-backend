import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'aol.settings')
from django.conf import settings

app = Celery('aol')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
