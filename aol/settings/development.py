import os.path

from .base import *


DEBUG = True
DEBUG_PROPOGATE_EXCEPTIONS = DEBUG
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = ['127.0.0.1', '172.20.0.1']

MEDIA_ROOT = os.path.join(FILE_ROOT, 'media')
STATIC_ROOT = os.path.join(FILE_ROOT, 'static')

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = False

CORS_ORIGIN_ALLOW_ALL = True

idx = MIDDLEWARE.index('django.middleware.common.CommonMiddleware')
MIDDLEWARE.insert(idx, 'corsheaders.middleware.CorsMiddleware')
INSTALLED_APPS.append('corsheaders')

DATABASES['default']['HOST'] = '172.20.0.1'
DATABASES['default']['USER'] = 'aol'
DATABASES['default']['PASSWORD'] = 'aol'
DATABASES['default']['NAME'] = 'aol'

# DATABASES['mussels']['HOST'] = '172.20.0.1'
# DATABASES['mussels']['USER'] = 'aol'
# DATABASES['mussels']['PASSWORD'] = 'aol'
# DATABASES['mussels']['NAME'] = 'aol'

CELERY_BROKER_URL = 'pyamqp://guest:guest@172.20.0.1//'  # rabbitmq//'
