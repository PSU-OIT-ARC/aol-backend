from model_mommy.mommy import make
from mommy_spatial_generators.generators import *

from ..models import LakeGeom, NHDLake as Lake


def make_lake(lake_kwargs=None, geom_kwargs=None):

    kwargs = {'title': "Oregon Lake",
              'ftype': 390,
              'is_in_oregon': True}
    if lake_kwargs is not None:
        kwargs.update(lake_kwargs)
    lake = make(Lake,**kwargs)

    kwargs = {'reachcode': lake,
              'the_geom': gen_rectangular_multipolygon(srid=3644)}
    if geom_kwargs is not None:
        kwargs.update(geom_kwargs)
    geom = make(LakeGeom, **kwargs)

    return (lake, geom)
