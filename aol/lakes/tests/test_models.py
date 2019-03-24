from django.test import TestCase
from model_mommy.mommy import make

from ..models import HUC6, LakeCounty, NHDLake as Lake
from . import make_lake


class LakeManagerTest(TestCase):
    def test_get_query_set(self):
        (lake, geom) = make_lake(lake_kwargs={'title': "Matt Lake"})
        make(LakeCounty, lake=lake, county__name="Clark")
        make(LakeCounty, lake=lake, county__name="Washington")

        # the lake should have a comma separated list of counties as
        # loading the instance should cache the computed 'counties' attribute.
        lake = Lake.objects.get(pk=lake.pk)
        with self.assertNumQueries(0):
            # the ordering matters here. It's alphabetical
            self.assertTrue(lake.counties, "Clark, Washington")

    def test_search(self):
        for title in ["Matt Lake", "Bob Lake"]:
            (lake, geom) = make_lake(lake_kwargs={'title':title})
        lakes = Lake.objects.search("")[:2]
        self.assertTrue(len(lakes), 2)

    def test_to_kml(self):
        # make sure invalid scales raise errors
        invalid_scale = 12
        self.assertRaises(ValueError, Lake.objects.to_kml, scale=invalid_scale, bbox=())

        lakes = Lake.objects.to_kml(scale=108000, bbox=(-50000, -50000, 50000, 50000))
        for lake in lakes:
            # make sure the lake has a kml attribute set
            self.assertTrue(lake.kml)


class LakeTest(TestCase):
    def test_area(self):
        (lake, geom) = make_lake()
        self.assertTrue(lake.area)
        # check to make sure we cache the result
        with self.assertNumQueries(0):
            self.assertTrue(lake.area)

    def test_perimeter(self):
        (lake, geom) = make_lake()
        self.assertTrue(lake.perimeter)
        # check to make sure we cache the result
        with self.assertNumQueries(0):
            self.assertTrue(lake.perimeter)

    def test_bounding_box(self):
        (lake, geom) = make_lake()
        self.assertTrue(lake.bounding_box)
        # check to make sure we cache the result
        with self.assertNumQueries(0):
            self.assertTrue(lake.bounding_box)

    def test_counties(self):
        (lake, geom) = make_lake(lake_kwargs={'title': "Matt Lake"})
        make(LakeCounty, lake=lake, county__name="Clark")
        make(LakeCounty, lake=lake, county__name="Washington")

        # the lake should have a comma separated list of counties as
        # loading the instance should cache the computed 'counties' attribute.
        lake = Lake.objects.get(pk=lake.pk)
        self.assertEqual(lake.counties, "Clark, Washington")
        # check to make sure we cache the result
        with self.assertNumQueries(0):
            self.assertEqual(lake.counties, "Clark, Washington")

        # test the setter
        lake.counties = "foo"
        self.assertEqual(lake.counties, "foo")

    def test_watershed_tile_url(self):
        huc6 = make(HUC6, the_geom="MULTIPOLYGON (((30.0000000000000000 20.0000000000000000, 10.0000000000000000 40.0000000000000000, 45.0000000000000000 40.0000000000000000, 30.0000000000000000 20.0000000000000000)), ((15.0000000000000000 5.0000000000000000, 40.0000000000000000 10.0000000000000000, 10.0000000000000000 20.0000000000000000, 5.0000000000000000 10.0000000000000000, 15.0000000000000000 5.0000000000000000)))")  # noqa

        (lake, geom) = make_lake(lake_kwargs={'title':"Matt Lake"},
                                 geom_kwargs={'the_geom': "MULTIPOLYGON (((30.0000000000000000 20.0000000000000000, 10.0000000000000000 40.0000000000000000, 45.0000000000000000 40.0000000000000000, 30.0000000000000000 20.0000000000000000)), ((15.0000000000000000 5.0000000000000000, 40.0000000000000000 10.0000000000000000, 10.0000000000000000 20.0000000000000000, 5.0000000000000000 10.0000000000000000, 15.0000000000000000 5.0000000000000000)))"})

        # just make sure the URL has a bbox set in it
        lake = Lake.objects.get(title="Matt Lake")
        url = lake.watershed_tile_url
        self.assertTrue("?bbox=-295,-295,345,340" in url)

    def test_basin_tile_url(self):
        (lake, geom) = make_lake(lake_kwargs={'title':"Matt Lake"},
                                 geom_kwargs={'the_geom': "MULTIPOLYGON (((30.0000000000000000 20.0000000000000000, 10.0000000000000000 40.0000000000000000, 45.0000000000000000 40.0000000000000000, 30.0000000000000000 20.0000000000000000)), ((15.0000000000000000 5.0000000000000000, 40.0000000000000000 10.0000000000000000, 10.0000000000000000 20.0000000000000000, 5.0000000000000000 10.0000000000000000, 15.0000000000000000 5.0000000000000000)))"})

        # just make sure the URL has a bbox set in it
        lake = Lake.objects.get(title="Matt Lake")
        url = lake.basin_tile_url
        self.assertTrue("?bbox=-995,-995,1045,1040" in url)
