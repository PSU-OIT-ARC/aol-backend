import os.path

from django.test.runner import DiscoverRunner
from django.db import connection

from model_mommy.mommy import generators
from mommy_spatial_generators import MOMMY_SPATIAL_FIELDS


class TestRunner(DiscoverRunner):
    """
    Loads out-of-scope schema which is managed by a separate project.
    """
    def __register_geospatial_generators(self):
        """
        Registers model_mommy generators from 'mommy_spatial_generators'.
        """
        for _type, gen in MOMMY_SPATIAL_FIELDS.items():
            generators.add(_type, gen)

    def __load_mussels_schema_sql(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'create-mussels-schema.sql')
        cursor = connection.cursor()

        with open(path, 'r') as f:
            cursor.execute(f.read())

    def setup_test_environment(self, **kwargs):
        super().setup_test_environment(**kwargs)
        self.__register_geospatial_generators()

    def setup_databases(self, *args, **kwargs):
        to_return = super().setup_databases(*args, **kwargs)
        self.__load_mussels_schema_sql()
        return to_return
