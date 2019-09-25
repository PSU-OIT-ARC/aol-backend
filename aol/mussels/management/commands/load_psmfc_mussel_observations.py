"""
Call this command like ./manage.py load_imap_plant_observations path/to/csv.csv

CSV may be obtains from:
http://psmfc.maps.arcgis.com/apps/webappviewer/index.html

The required columns are:
  - Collecting Agency
  - Target
  - Sample Collection Method
  - Date Sampled
  - REACHCODE
"""
import dateparser
import dateutil
import csv
import sys

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError, transaction
from django.db.models import Q

from aol.lakes.models import Lake
from aol.mussels.models import Mussel, MusselObservation
from aol.mussels import enums


class Command(BaseCommand):
    help = "Import mussel data from the PSMFC export CSV"

    def add_arguments(self, parser):
        parser.add_argument('csv', type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        existing_lakes = set(Lake.objects.filter(has_plants=True).values_list('pk', flat=True))
        updated_lakes = set()

        # Delete all extant observations (each dataset is considered the full dataset)
        MusselObservation.objects.all().delete()

        with open(options['csv'], 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                with transaction.atomic():
                    try:
                        # Create or update the given mussel record
                        mussel = None
                        # (mussel, _) = Mussel.objects.update_or_create(
                        #     machine_name=row['Machine Name'].lower(),
                        #     defaults={'name': row['Name'],
                        #               'machine_name': row['Machine Name']})

                        # Fetch the associated lake
                        lake = Lake.objects.get(Q(reachcode=row['REACHCODE']) | Q(permanent_id=row['PERMANENT_IDENTIFIER']))
                        # Create a new observation record for this row data
                        MusselObservation.objects.update_or_create(
                            lake=lake,
                            mussel=mussel,
                            date_sampled=dateparser.parse(row['Date Sampled']),
                            target=row['Target'],
                            collection_method=row['Sample Collection Method'],
                            collecting_agency=row['Collecting Agency'],
                            defaults={'status': enums.STATUS_NON_DETECT})
                        # Record lake as it has been updated
                        updated_lakes.add(lake)
                    except Lake.DoesNotExist:
                        log_args = (row['REACHCODE'], row['PERMANENT_IDENTIFIER'])
                        print("Lake with reachcode '{}' or permanent ID '{}' not found".format(*log_args))
                    except ValueError:
                        print("Point coordinates '{}, {}' are invalid or not given".format(row['x'], row['y']))

            # Marks updated lakes as having mussel observation data
            queryset = Lake.objects.filter(pk__in=[l.pk for l in updated_lakes])
            print("Updating {} lakes with mussel observation data.".format(queryset.count()))
            queryset.update(has_mussels=True)

            # Marks those lakes not updated as not having observation data
            queryset = Lake.objects.filter(pk__in=existing_lakes)
            print("Clearing {} lakes without mussel observation data.".format(queryset.count()))
            queryset.update(has_mussels=False)
