# -*- coding: utf-8 -*-
import os.path

from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

from .paths import *


# TODO: Settings to review
# 
# DISTRIBUTION = "psu.oit.arc.aol"
# PROJECT.title = "Atlas of Oregon Lakes"
# PROJECT.short_title = "AOL"

WSGI_APPLICATION = 'aol.wsgi.application'
ROOT_URLCONF = 'aol.urls'
SITE_ID = 1

# Email/correspondence settings
SERVER_EMAIL = 'do-not-reply@wdt.pdx.edu'
DEFAULT_FROM_EMAIL = SERVER_EMAIL
EMAIL_SUBJECT_PREFIX = "[Atlas of Oregon Lakes] "
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_ETAGS = True
USE_I18N = True
USE_L10N = True
USE_TZ = True


SECRET_KEY = 'NOTASECRET'

# CSRF Defaults
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True

# Google Analytics
# GOOGLE.analytics.tracking_id = null

# ArcGIS Online
ARCGIS_ONLINE_TOKEN_URL = 'https://www.arcgis.com/sharing/rest/oauth2/token'

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', )
LOGIN_URL = reverse_lazy('social:begin')
LOGIN_REDIRECT_URL = reverse_lazy('admin:index')
SOCIAL_AUTH_LOGIN_ERROR_URL = reverse_lazy('admin:login')
SOCIAL_AUTH_WHITELISTED_DOMAINS = ('pdx.edu', )
SOCIAL_AUTH_POSTGRES_JSONFIELD = True
SOCIAL_AUTH_PIPELINE = [
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'aol.backend.auth.has_existing_account',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data'
]

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_PATH, 'templates')],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            "django.template.context_processors.csrf",
            "django.template.context_processors.debug",
            "django.template.context_processors.i18n",
            "django.template.context_processors.media",
            "django.template.context_processors.request",
            "django.template.context_processors.static",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
            'social_django.context_processors.backends',
            'social_django.context_processors.login_redirect',
        ]
    }
}]

MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]

INSTALLED_APPS = [
    'django.contrib.admin.apps.SimpleAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.messages',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    'social_django',
    'django_filters',
    'rest_framework',
    'ckeditor',

    'aol.apps.MainAppConfig',
    'aol.lakes',
    'aol.documents',
    'aol.resources',
    'aol.photos',
    'aol.plants',
    'aol.mussels'
]

REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': None
}

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_PATH, '.cache')
    }
}

CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = TIME_ZONE
# CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_ALWAYS_EAGER = False
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_SEND_TASK_ERROR_EMAILS = True

CELERY_ACCEPT_CONTENT = ['json', 'pickle']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
## Celeryd settings
CELERY_WORKER_CONCURRENCY = 1
## Result store settings
CELERY_TASK_IGNORE_RESULT = True
## Celerybeat settings
CELERY_BEAT_SCHEDULER = 'celery.beat.PersistentScheduler'
