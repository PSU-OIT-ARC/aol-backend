import os.path

from django.test.runner import DiscoverRunner
from django.db import connection

from model_mommy.mommy import generators


class TestRunner(DiscoverRunner):
    """
    Loads out-of-scope schema which is managed by a separate project.
    """
    def __load_mussels_schema_sql(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'create-mussels-schema.sql')
        cursor = connection.cursor()

        with open(path, 'r') as f:
            cursor.execute(f.read())

    def setup_databases(self, *args, **kwargs):
        to_return = super().setup_databases(*args, **kwargs)
        self.__load_mussels_schema_sql()
        return to_return
