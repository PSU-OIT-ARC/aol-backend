#!/vol/www/aol/builds/prod/1.3.2/.env/bin/python
import csv
import sys
import os

import django
from django.apps import apps
from django.db import connection


EXPORT_LIMIT = 100000
EXPORT_MODELS = [
    ('lakes.County', ['county_id', 'name'], 'counties.csv'),
    ('lakes.LakeCounty', ['lake_county_id', 'lake_id', 'county_id'], 'lake_counties.csv'),
    ('lakes.FishingZone', ['fishing_zone_id', 'odfw'], 'fishing_zones.csv'),
    ('lakes.NHDLake', ['title', 'aol_page', 'body',
                      'reachcode', 'parent_id', 'permanent_id', 'gnis_id', 'gnis_name',
                      'fishing_zone_id'], 'lakes.csv'),
    ('photos.Photo', ['lake_id', 'photo_id', 'file', 'taken_on', 'author', 'caption'], 'photos.csv'),
    ('documents.Document', ['lake_id', 'document_id', 'name', 'file', 'rank', 'uploaded_on', 'type', 'friendly_filename'], 'documents.csv'),
]


def __get_instance_attr(instance, field):
    for part in field.split('.'):
        instance = getattr(instance, part)
    return instance


def export_legacy_data():
    for model_spec, fields, output_file in EXPORT_MODELS:
        queryset = apps.get_model(model_spec).objects.all()
        print("Exporting {} {} objects...".format(queryset.count(), queryset.model._meta.verbose_name))

        cnt = 0
        with open(output_file, 'w') as f:
            archive = csv.writer(f, quoting=csv.QUOTE_ALL)
            archive.writerow(fields)
            for instance in queryset.iterator():
                row = [__get_instance_attr(instance, field) for field in fields]
                archive.writerow(row)
                cnt += 1

        print("Exported {} records.".format(cnt))


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aol.settings')
    django.setup()
    export_legacy_data()
