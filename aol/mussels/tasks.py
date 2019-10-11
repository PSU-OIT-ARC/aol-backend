import datetime
import sys
import io

from django.core.management import call_command
from django.db import transaction

from celery.utils.log import get_task_logger

from aol.mussels.models import ImportedMusselObservation
from aol.mussels import enums
from aol.celery import app

logger = get_task_logger(__name__)


@app.task
def import_mussel_observation_datafile(**kwargs):
    record = ImportedMusselObservation.objects.get(pk=kwargs.get('pk'))
    record.status = enums.IMPORT_STATUS_LOADING
    record.output = ''
    record.save()

    (_stdout, _stderr) = (sys.stdout, sys.stderr)
    (sys.stdout, sys.stderr) = (io.StringIO(), io.StringIO())

    try:

        call_command('load_psmfc_mussel_observations', record.datafile.path)
        record.status = enums.IMPORT_STATUS_COMPLETED
    except Exception as exc:
        record.status = enums.IMPORT_STATUS_ERROR
        sys.stderr.write("Error during import: {}".format(str(exc)))

    record.output = '{}\n{}'.format(sys.stdout.getvalue(), sys.stderr.getvalue())
    record.save()

    sys.stdout = _stdout
    sys.stderr = _stderr
