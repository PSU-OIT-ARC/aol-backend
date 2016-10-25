from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from arcutils.cas import urls as cas_urls
from arcutils.cas import views as cas_views

from aol.documents import views as documents
from aol.home import views as home
from aol.lakes import views as lakes
from aol.maps import views as maps
from aol.photos import views as photos
from aol.users import views as customadmin

urlpatterns = [
    url(r'^$', home.home, name='home'),
    url(r'^search/?$', lakes.search, name='lakes-search'),

    url(r'^lakes/?$', lakes.listing, name='lakes-listing'),
    url(r'^lakes/(?P<letter>[a-z])/?$', lakes.listing, name='lakes-listing'),
    url(r'^lakes/(?P<reachcode>.+)?$', lakes.detail, name='lakes-detail'),
    url(r'^plants/csv/(?P<reachcode>.+)?$', lakes.plants_csv, name='plants-csv'),

    url(r'^map/?$', maps.home, name='map'),
    url(r'^map/search/?$', maps.search, name='map-search'),
    url(r'^map/lakes\.kml$', maps.lakes, name='lakes-kml'),
    url(r'^map/facilities\.kml$', maps.facilities, name='facilities-kml'),
    url(r'^maps/panel/(?P<reachcode>.+)?$', maps.panel, name='lakes-panel'),

    # CAS Authentication
    url(r'^accounts/login/$', cas_views.login, name='login'),
    url(r'^accounts/logout/$', cas_views.logout, name='logout'),
    url(r'^accounts/validate/$', cas_views.validate, name='cas-validate'),

    # Admin area
    url(r'^admin/?$', customadmin.listing, name='admin-listing'),
    url(r'^admin/edit/lake/(?P<reachcode>.+)?$', customadmin.edit_lake, name='admin-edit-lake'),
    url(r'^admin/edit/photo/(?P<photo_id>\d+)?$', photos.edit, name='admin-edit-photo'),
    url(r'^admin/edit/flatpage/(?P<pk>\d+)?$', customadmin.edit_flatpage, name='admin-edit-flatpage'),
    url(r'^admin/add/photo/(?P<reachcode>.+)?$', photos.edit, name='admin-add-photo'),
    url(r'^admin/edit/document/(?P<document_id>\d+)?$', documents.edit, name='admin-edit-document'),
    url(r'^admin/add/document/(?P<reachcode>.+)?$', documents.edit, name='admin-add-document'),
    url(r'^admin/add/flatpage/?$', customadmin.edit_flatpage, name='admin-add-flatpage'),

    # documents
    url(r'^documents/download/(?P<document_id>.+)?$', documents.download, name='documents-download'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
