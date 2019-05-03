import functools

from arcutils.settings import init_settings
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


init_settings(settings_processors=[processors.set_secret_key,
                                   processors.set_database_parameters,
                                   configure_sentry_sdk])
