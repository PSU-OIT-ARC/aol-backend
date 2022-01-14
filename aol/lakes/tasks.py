from django.core.management import call_command

from aol.celery import app


@app.task
def cache_lakes():
    call_command('cache_lakes')
