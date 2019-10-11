"""
Call this command like ./manage.py load_imap_plant_observations path/to/csv.csv

CSV may be obtained from:
https://imapinvasives.natureserve.org/imap/services/page/map.html

The required columns are:
  - x
  - y
  - scientific_name
  - common_name
  - observation_date
  - organization_name
"""
import dateparser
import dateutil
import csv
import sys

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError, transaction

from aol.lakes.models import Lake
from aol.plants.models import Plant, PlantObservation
from aol.plants import enums


class Command(BaseCommand):
    help = "Import plant data from the iMapInvasives export CSV"

    def add_arguments(self, parser):
        parser.add_argument('csv', type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        # Delete all extant IMAP observations (each dataset is considered the full dataset)
        PlantObservation.objects.filter(source=enums.REPORTING_SOURCE_IMAP).delete()
        # Mark all applicable lakes as having no plant observations
        Lake.objects.filter(plant_observations__isnull=True, has_plants=True).update(has_plants=False)

        with open(options['csv'], 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                with transaction.atomic():
                    try:
                        # Create or update the given plant record
                        (plant, _) = Plant.objects.update_or_create(
                            normalized_name=row['scientific_name'].lower(),
                            defaults={'name': row['scientific_name'],
                                      'common_name': row['common_name'].title()})

                        # Fetch the associated lakes
                        lakes = Lake.objects.get_for_point(float(row['x']), float(row['y']))
                        for lake in lakes.iterator():
                            # Create a new observation record for this row data
                            PlantObservation.objects.update_or_create(
                                lake=lake,
                                plant=plant,
                                observation_date=dateparser.parse(row['observation_date']),
                                defaults={'source': enums.REPORTING_SOURCE_IMAP,
                                          'survey_org': row['organization_name']})
                    except ValueError:
                        print("Point coordinates '{}, {}' are invalid or not given".format(row['x'], row['y']))
