#!.env/bin/python
import csv
import sys
import os

import django
from django.apps import apps
from django.db import transaction
from django.db.models import Q


IMPORT_ARCHIVE_PATH = 'legacy_data'
IMPORT_MODELS = {
    'lakes.County': ['county_id', 'name'],
    'lakes.LakeCounty': ['lake_county_id', 'lake_id', 'county_id'],
    'lakes.FishingZone': ['fishing_zone_id', 'odfw'],
    'lakes.Lake': ('title', 'aol_page', 'body',
                   'reachcode', 'parent_id', 'permanent_id', 'gnis_id', 'gnis_name',
                   'fishing_zone_id'),
    'photos.Photo': ['lake_id', 'photo_id', 'file', 'taken_on', 'author', 'caption'],
    'documents.Document': ['lake_id', 'document_id', 'name', 'file', 'rank', 'uploaded_on', 'type', 'friendly_filename'],
}

def import_csv(input_file, fields, callback):
    print("Importing '{}' with fields {}".format(input_file, fields))
    input_path = os.path.join(IMPORT_ARCHIVE_PATH, input_file)
    with open(input_path, 'r') as f:
        archive = csv.DictReader(f, fieldnames=fields)
        archive.__next__()
        with transaction.atomic():
            for row in archive:
                row = {k:v for k,v in row.items() if v}
                callback(row)


def import_lookup_models():
    from aol.lakes.models import County, FishingZone

    def import_county(row):
        row['pk'] = row.pop('county_id')
        County.objects.update_or_create(defaults=row, **row)
    import_csv('counties.csv',
               IMPORT_MODELS.get('lakes.County'),
               import_county)

    def import_fishing_zone(row):
        row['pk'] = row.pop('fishing_zone_id')
        FishingZone.objects.update_or_create(defaults=row, **row)
    import_csv('fishing_zones.csv',
               IMPORT_MODELS.get('lakes.FishingZone'),
               import_fishing_zone)


def import_lakes():
    from aol.lakes.models import Lake

    def import_lake(row):
        try:
            queryset = Lake.all_objects.filter(Q(reachcode=row.get('reachcode')) |
                                               Q(permanent_id=row.get('permanent_id')) |
                                               Q(gnis_id=row.get('gnis_name')))
            if not queryset.exists():
                print("Processing unknown lake {}".format(row))
                row['title'] = '{} (Legacy)'.format(row.get('title', ''))
                Lake.all_objects.create(**row)
                return
            Lake.objects.update_or_create(defaults=row, pk=row.get('reachcode'))
        except Exception as e:
            print("An error occurred while importing lake '{}': {}".format(row, str(e)))
    import_csv('lakes.csv',
               IMPORT_MODELS.get('lakes.Lake'),
               import_lake)


def import_membership_models():
    from aol.lakes.models import County, Lake

    def import_lake_counties(row):
        try:
            if 'lake_id' not in row:
                print("No lake reference for county membership: {}".format(row))
                return
            lake = Lake.all_objects.get(pk=row['lake_id'])
            county = County.objects.get(pk=row['county_id'])
            lake.county_set.add(county)
        except Lake.DoesNotExist:
            print("Lake given by '{}' does not exist".format(row['lake_id']))
        except County.DoesNotExist:
            print("County given by '{}' does not exist".format(row['county_id']))
    import_csv('lake_counties.csv',
               IMPORT_MODELS.get('lakes.LakeCounty'),
               import_lake_counties)


def import_related_models():
    from aol.lakes.models import Lake
    from aol.documents.models import Document
    from aol.photos.models import Photo

    def import_documents(row):
        try:
            if 'lake_id' not in row:
                print("No lake reference for document: {}".format(row))
                return
            lake = row['lake'] = Lake.all_objects.get(pk=row['lake_id'])
            row['pk'] = row.pop('document_id')
            (document, created) = Document.objects.update_or_create(defaults=row, **row)
            lake.documents.add(document)
        except Lake.DoesNotExist:
            print("Lake given by '{}' does not exist".format(row['lake_id']))
    import_csv('documents.csv',
               IMPORT_MODELS.get('documents.Document'),
               import_documents)

    def import_photos(row):
        try:
            if 'lake_id' not in row:
                print("No lake reference for photo: {}".format(row))
                return
            lake = row['lake'] = Lake.all_objects.get(pk=row['lake_id'])
            row['pk'] = row.pop('photo_id')
            (photo, created) = Photo.objects.update_or_create(defaults=row, **row)
            lake.photos.add(photo)
        except Lake.DoesNotExist:
            print("Lake given by '{}' does not exist".format(row['lake_id']))
    import_csv('photos.csv',
               IMPORT_MODELS.get('photos.Photo'),
               import_photos)


if __name__ == '__main__':
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aol.settings')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aol.settings.development')
    django.setup()

    import_lookup_models()
    import_lakes()
    import_membership_models()
    import_related_models()
