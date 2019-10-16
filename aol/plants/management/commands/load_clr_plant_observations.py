"""
Call this command like ./manage.py load_clr_plant_observations path/to/csv.csv

CSV may be obtained from:
Rich Miller <richm@pdx.edu>

The required columns are:
  - ScientificName
  - CommonName
  - NoxiousWeedDesignation,
  - NativeSpecies
  - ObsDate
  - Reachcode
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
    help = "Import plant data from the Rich Miller's CLR plant export CSV"

    def add_arguments(self, parser):
        parser.add_argument('csv', type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        # Delete all extant CLR observations (each dataset is considered the full dataset)
        PlantObservation.objects.filter(source=enums.REPORTING_SOURCE_CLR).delete()
        # Mark all applicable lakes as having no plant observations
        Lake.active.filter(plant_observations__isnull=True, has_plants=True).update(has_plants=False)

        with open(options['csv'], 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                with transaction.atomic():
                    try:
                        # Create or update the given plant record
                        (plant, _) = Plant.objects.update_or_create(
                            normalized_name=row['ScientificName'].lower(),
                            defaults={'name': row['ScientificName'],
                                      'common_name': row['CommonName'].title(),
                                      'noxious_weed_designation': row['NoxiousWeedDesignation'],
                                      'is_native': row['NativeSpecies'] == "1"})

                        # Fetch the associated lake
                        lake = Lake.active.get(pk=int(float(row['ReachCode'])))
                        # Create a new observation record for this row data
                        PlantObservation.objects.update_or_create(
                            lake=lake,
                            plant=plant,
                            observation_date=dateparser.parse(row['ObsDate']),
                            defaults={'source': enums.REPORTING_SOURCE_CLR,
                                      'survey_org': row['SurveyOrg']})
                    except Lake.DoesNotExist:
                        print("Lake with reachcode '{}' not found".format(int(float(row['ReachCode']))))
                    except ValueError:
                        print("Reachcode '{}' invalid or not given".format(row['ReachCode']))
