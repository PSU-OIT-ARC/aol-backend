import shapefile
from shapely.geometry import asShape

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from django.db import transaction

from aol.lakes.models import Lake


class Command(BaseCommand):
    help = 'Load a shapefile'

    def add_arguments(self, parser):
        parser.add_argument('shapefile', type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        # read the shapefile
        print("Assuming shapefile uses srid/epsg 4269!")
        sf = shapefile.Reader(options['shapefile'])

        # the first field is the DeleteFlg, which isn't stored in the actual
        # records, so we cut it off
        fields = sf.fields[1:]

        # the fields *should* be labeled as such, so we use these keys to index
        # the record dictionary
        # ['Permanent_', 'FDate', 'Resolution', 'GNIS_ID', 'GNIS_Name',
        # 'AreaSqKm', 'Elevation', 'ReachCode', 'FType', 'FCode', 'Shape_Leng',
        # 'Shape_Area', 'AOLReachCo', 'AOLGNIS_Na']

        # for shape, record in itertools.izip(sf.iterShapes(), sf.iterRecords()):
        cnt= 0
        for shape, record in zip(sf.iterShapes(), sf.iterRecords()):
            # if cnt > 10000:
            #     print("Processed 1000 entries. Exiting.")
            #     return

            # make it so we can index by column name instead of column position
            record = dict((field_description[0].upper(), field_value)
                          for field_description, field_value in zip(fields, record))
            if record['REACHCODE'].strip() == "":
                print("Skipping lake with no reachcode and permanent_id=%s" % record['PERMANENT_'].strip())
                continue

            print("Creating or updating lake: {}".format(record))

            # this stupid pyshp library has no way to spit out the wkt
            # which is what GEOSGeometry needs, so we have to rely on
            # another library to do the conversion
            geom = GEOSGeometry(asShape(shape).wkt, srid=4269)
            # cast polygons to multipolygons
            if geom.geom_type == "Polygon":
                geom = MultiPolygon(geom, srid=4269)
            # transform geometry to appropriate SRID
            geom.transform(3644)

            (lake, created) = Lake.objects.update_or_create(
                reachcode=record['REACHCODE'],
                defaults = {
                    'permanent_id': record['PERMANENT_'].strip(),
                    'gnis_id': record['GNIS_ID'].strip(),
                    'gnis_name': record['GNIS_NAME'].strip(),
                    'waterbody_type': record['FTYPE'],
                    'the_geom': geom,
                }
            )
            cnt += 1
