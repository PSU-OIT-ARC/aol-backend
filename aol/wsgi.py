import os
import site
import sys


def create_wsgi_application(root, settings_module=None, local_settings_file=None):
    """Create a WSGI application anchored at ``root``.

    ``settings_module`` is only used if the ``DJANGO_SETTINGS_MODULE``
    environment variable is not already set.

    Likewise, ``local_settings_file`` is only used if the environment
    variable ``LOCAL_SETTINGS_FILE`` is not already set. The default
    value for this is ``{root}/local.cfg``. If a project doesn't use
    ``django-local-settings``, this will have no effect.

    """
    if local_settings_file is None:
        local_settings_file = os.path.join(root, 'local.cfg')

    os.environ.setdefault('LOCAL_SETTINGS_FILE', local_settings_file)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

    from django.core.wsgi import get_wsgi_application
    return get_wsgi_application()


root = os.path.dirname(os.path.dirname(__file__))
settings_module = 'aol.settings'
application = create_wsgi_application(root, settings_module)
