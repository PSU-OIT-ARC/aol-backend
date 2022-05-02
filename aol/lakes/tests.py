from django.test import TestCase

from model_mommy.mommy import make

from aol.lakes.models import County, Lake



def make_lake(lake_kwargs=None):
    params = dict(
        title="Matt Lake",
        the_geom="MULTIPOLYGON (((30.0000000000000000 20.0000000000000000, 10.0000000000000000 40.0000000000000000, 45.0000000000000000 40.0000000000000000, 30.0000000000000000 20.0000000000000000)), ((15.0000000000000000 5.0000000000000000, 40.0000000000000000 10.0000000000000000, 10.0000000000000000 20.0000000000000000, 5.0000000000000000 10.0000000000000000, 15.0000000000000000 5.0000000000000000)))"
    )
    if lake_kwargs is not None:
        params.update(lake_kwargs)

    lake = make(Lake, **params)
    for name in ('Clark', 'Washington'):
        county = make(County, name=name)
        lake.county_set.add(county)
    return lake


class LakeTestCase(TestCase):
    def setUp(self):
        super().setUp()

        self.lake = make_lake()

    def test_area(self):
        self.assertTrue(self.lake.area)

    def test_shoreline(self):
        self.assertTrue(self.lake.shoreline)

    def test_counties(self):
        # the lake should have a comma separated list of counties as
        # loading the instance should cache the computed 'counties' attribute.
        # the ordering matters here. It's alphabetical
        self.assertEqual(self.lake.counties, "Clark, Washington")

        # test the setter
        self.lake.counties = "foo"
        self.assertEqual(self.lake.counties, "foo")
