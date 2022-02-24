# -*- coding: utf-8 -*-
import datetime
import os.path

from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

from celery.schedules import crontab

from emcee.runner.config import YAMLCommandConfiguration
from emcee.runner import configs, config
from emcee.app.config import YAMLAppConfiguration, load_app_configuration
from emcee.app import app_configs, app_config, processors

configs.load(YAMLCommandConfiguration)
app_configs.load(YAMLAppConfiguration)


BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FILE_ROOT = os.path.abspath(os.path.join(BASE_PATH, '..'))

WSGI_APPLICATION = 'aol.wsgi.application'
ROOT_URLCONF = 'aol.urls'
SITE_ID = 1

# Email/correspondence settings
SERVER_EMAIL = 'do-not-reply@oregonlakesatlas.org'
DEFAULT_FROM_EMAIL = SERVER_EMAIL
ADMINS = [["PSU Web & Mobile Team", "webteam@pdx.edu"]]
MANAGERS = [["PSU Web & Mobile Team", "webteam@pdx.edu"]]
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

# CSRF Defaults
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True

STATIC_ROOT = os.path.join(FILE_ROOT, 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(FILE_ROOT, 'media')
MEDIA_URL = '/media/'
SENDFILE_ROOT = MEDIA_ROOT
SENDFILE_URL = MEDIA_URL

# Logging configuration
FIRST_PARTY_LOGGER = {
    'handlers': ['console'],
    'propagate': False,
    'level': 'INFO'
}
THIRD_PARTY_LOGGER = {
    'handlers': ['console'],
    'propagate': False,
    'level': 'WARN'
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s [%(name)s] %(message)s'
        }
    },
    'filters': {},
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'aol': FIRST_PARTY_LOGGER,
        'celery.task': FIRST_PARTY_LOGGER,
        'django': THIRD_PARTY_LOGGER,
    },
    'root': THIRD_PARTY_LOGGER
}

LOGIN_URL = reverse_lazy('social:begin')
LOGIN_REDIRECT_URL = reverse_lazy('admin:index')

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', )
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
    'django_sendfile',
    'robots',

    'aol.apps.MainAppConfig',
    'aol.lakes',
    'aol.documents',
    'aol.resources',
    'aol.photos',
    'aol.plants',
    'aol.mussels'
]

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

CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_ALWAYS_EAGER = False
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_SEND_TASK_ERROR_EMAILS = True

# TODO: Verify removal of 'pickle' serializer
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
## Celeryd settings
CELERY_WORKER_CONCURRENCY = 1
## Result store settings
CELERY_TASK_IGNORE_RESULT = True
## Celerybeat settings
CELERY_BEAT_SCHEDULER = 'celery.beat.PersistentScheduler'

CELERY_BEAT_SCHEDULE = {
    ## Caches lake index data
    ## Every hour
    "cache_lakes": {
        "task": "aol.lakes.tasks.cache_lakes",
        "schedule": datetime.timedelta(hours=1)
    },

    ## Clears expired sessions
    ## 3:00 a.m.
    "clear_expired_sessions": {
        "task": "aol.tasks.clear_expired_sessions",
        "schedule": crontab(hour=3, minute=0),
    },
}

# Application-specific configuration
ARCGIS_ONLINE_TOKEN_URL = 'https://www.arcgis.com/sharing/rest/oauth2/token'
GOOGLE_ANALYTICS_TRACKING_ID = None

# Configure environment-specific configuration
if config.env in ['stage', 'prod']:
    # Instruct Django to inspect HTTP header to help determine
    # whether the request was made securely
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

elif config.env in ['dev', 'docker']:
    # Enable installed apps, middleware for development environments
    if os.environ.get('APP_SERVICE') == 'wsgi':
        INSTALLED_APPS.append('corsheaders')
        MIDDLEWARE.insert(3, 'corsheaders.middleware.CorsMiddleware')

    # Configure 'INTERNAL_IPS' to support development environments
    import ipaddress

    class CIDRList(object):
        addresses = [
            "127.0.0.0/8",
            "169.254.0.0/16",  # RFC 3927/6890
            "10.0.0.0/8",  # RFC 1918
            "172.0.0.0/12",
            "192.168.0.0/16",
            "fe80::/10",
            "fd00::/8"  # RFC 7436
        ]

        def __init__(self):
            """Create a new ip_network object for each address range provided."""
            self.networks = [
                ipaddress.ip_network(address)
                for address in self.addresses
            ]

        def __contains__(self, address):
            """Check if the given address is contained in any of the networks."""
            return any([
                ipaddress.ip_address(address) in network
                for network in self.networks
            ])

    INTERNAL_IPS = CIDRList()

# Configure application secrets
settings = load_app_configuration(app_config, globals())
processors.set_secret_key(config, settings)
processors.set_database_parameters(config, settings)
processors.set_sentry_dsn(config, settings)
processors.set_smtp_parameters(config, settings)

# Configure ArcGIS credentials
ARCGIS_CLIENT_ID = processors.get_secret_value(config, 'ArcGISClientID')
ARCGIS_CLIENT_SECRET = processors.get_secret_value(config, 'ArcGISClientSecret')

# Configure Google OAuth2
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = processors.get_secret_value(config, 'GoogleOAuth2Secret')
