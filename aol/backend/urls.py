from django.urls import include, re_path as url

from rest_framework.schemas import get_schema_view
from rest_framework.renderers import JSONOpenAPIRenderer
from rest_framework import routers

from aol.lakes import views as lake_views
from aol.backend import views
from aol import __version__


# Schema
schema_view = get_schema_view(title='Atlas of Oregon Lakes API',
                              url='https://oregonlakesatlas.org',
                              version=__version__,
                              urlconf='aol.backend.urls',
                              renderer_classes=[JSONOpenAPIRenderer])

# Entry point for all API urls
app_name = 'backend'
urlpatterns = [
    url(r'^$', schema_view),
    url(r'^token/$', views.ArcGISAuthTokenView.as_view(), name='fetch-authtoken'),
    url(r'^flatpage/$', views.FlatPageListView.as_view(), name='flatpage-index'),
    url(r'^flatpage/(?P<slug>[-_\w]+)/$', views.FlatPageDetailView.as_view(), name='flatpage-detail'),
    url(r'^lake/$', lake_views.LakeListView.as_view(), name='lake-index'),
    url(r'^lake/(?P<pk>\d+)/$', lake_views.LakeDetailView.as_view(), name='lake-detail'),
]
