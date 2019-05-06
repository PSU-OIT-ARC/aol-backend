from .base import *


DEBUG = False
DEBUG_PROPOGATE_EXCEPTIONS = DEBUG
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ["aol-backend.wdt.pdx.edu"]
DEFAULT_FROM_EMAIL = "no-reply@wdt.pdx.edu"
ADMINS = [["PSU Web & Mobile Team", "webteam@pdx.edu"]]
MANAGERS = [["PSU Web & Mobile Team", "webteam@pdx.edu"]]

SSM_KEY = "vpc-prod/aol-backend"
AWS_REGION = "us-west-2"

AUTHENTICATION_BACKENDS = ('social_core.backends.google.GoogleOAuth2',
                           'django.contrib.auth.backends.ModelBackend')

STATIC_ROOT = "/vol/www/aol-backend/static/prod"
MEDIA_ROOT = "/vol/www/aol-backend/media/prod"

DATABASES['default']['HOST'] = ''
DATABASES['default']['NAME'] = 'aol'
DATABASES['default']['USER'] = 'aol_backend_l'

# DATABASES['mussels']['HOST'] = ''
# DATABASES['mussels']['NAME'] = 'aol'
# DATABASES['mussels']['USER'] = 'aol_l'


import functools

from emcee.backends.aws import processors
from sentry_sdk.integrations.django import DjangoIntegration
import sentry_sdk


def sentry_callback(settings, dsn):
    sentry_sdk.init(
        dsn=dsn,
        integrations=[DjangoIntegration()],
        debug=settings['DEBUG']
    )
configure_sentry_sdk = functools.partial(processors.set_sentry_dsn,
                                         callback=sentry_callback)

_configured_props = globals()
# print("_configured_props: {}".format(_configured_props))
processors.set_secret_key(_configured_props)
processors.set_database_parameters(_configured_props)
configure_sentry_sdk(_configured_props)
