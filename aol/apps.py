import importlib
import logging

from django.utils.module_loading import module_has_submodule
from django.apps import AppConfig
from django.apps import apps

logger = logging.getLogger(__name__)


def autoload_submodules(submodules):
    """
    Autoload the given submodules for all apps in INSTALLED_APPS.
    This utility was inspired by 'admin.autodiscover'.
    """
    for app in apps.get_app_configs():
        logger.debug("Analyzing app '%s' for modules '%s'" % (app, submodules))
        for submodule in submodules:
            dotted_path = "{0}.{1}".format(app.name, submodule)
            try:
                importlib.import_module(dotted_path)
            except:
                if module_has_submodule(app.module, submodule):
                    msg = "Trouble importing module '%s'"
                    logger.warn(msg % (dotted_path))
                    raise
            else:
                logger.debug("Imported module '%s'" % (dotted_path))


class MainAppConfig(AppConfig):
    name = 'aol'

    def ready(self):
        super().ready()

        autoload_submodules(['receivers'])
