from django.urls import include, re_path as url
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings

from rest_framework.authtoken import views

from aol.admin import admin_site


class IndexRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return '/admin/'

urlpatterns = [
    url(r'^$', IndexRedirectView.as_view(), name='index'),

    url(r'^api/', include('aol.backend.urls', namespace='api')),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^admin/', admin_site.urls),
    url(r'', include('social_django.urls', namespace='social')),
    url(r'^robots\.txt', include('robots.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
