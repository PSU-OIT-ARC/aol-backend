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
        existing_lakes = set(Lake.objects.filter(has_plants=True).values_list('pk', flat=True))
        updated_lakes = set()

        # Delete all extant IMAP observations (each dataset is considered the full dataset)
        PlantObservation.objects.filter(source=enums.REPORTING_SOURCE_IMAP).delete()

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
                            # Record lake as it has been updated
                            updated_lakes.add(lake)
                    except ValueError:
                        print("Point coordinates '{}, {}' are invalid or not given".format(row['x'], row['y']))

            # Marks updated lakes as having plant observation data
            queryset = Lake.objects.filter(pk__in=[l.pk for l in updated_lakes])
            print("Updating {} lakes with plant observation data.".format(queryset.count()))
            queryset.update(has_plants=True)

            # Evaluates those lakes not updated to determine whether they
            # have current plant observation data.
            queryset = Lake.objects.filter(pk__in=existing_lakes)
            queryset = queryset.exclude(pk__in=[l.pk for l in updated_lakes])
            print("Clearing {} lakes without plant observation data.".format(queryset.count()))
            for lake in queryset.iterator():
                lake.update_status()
                lake.save()
