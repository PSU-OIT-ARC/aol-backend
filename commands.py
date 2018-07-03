from emcee.runner.config import YAMLCommandConfiguration
from emcee.runner import command, configs, config
from emcee.runner.commands import remote
from emcee.runner.utils import confirm
from emcee.app.config import LegacyAppConfiguration
from emcee.app import app_configs
from emcee import printer

from emcee.commands.deploy import deploy
from emcee.commands.python import virtualenv, install
from emcee.commands.django import manage, manage_remote
from emcee.commands.javascript import npm_install

from emcee.provision.base import provision_host, patch_host
from emcee.provision.python import provision_python
from emcee.provision.services import provision_nginx
from emcee.provision.secrets import show_secret
from emcee.deploy.base import push_nginx_config
from emcee.deploy.python import push_uwsgi_ini, push_uwsgi_config, restart_uwsgi
from emcee.deploy.django import Deployer as DjangoDeployer

# from emcee.backends.dev.provision.db import provision_database as provision_database_local
from emcee.backends.aws.infrastructure.commands import *
from emcee.backends.aws.provision.db import provision_database

configs.load('default', 'commands.yml', YAMLCommandConfiguration)
app_configs.load('default', LegacyAppConfiguration)


@command(timed=True)
def init(overwrite=False):
    virtualenv(config.python.venv, overwrite=overwrite)
    install()
    npm_install()
    # provision_database_local(config, drop=drop_db, with_postgis=True)
    manage(('migrate', '--noinput'))


@command
def provision_app(createdb=False):
    # Configure host properties and prepare host platforms
    provision_host(initialize_host=True)
    provision_python()
    provision_nginx()

    if createdb:
        backend_options={'with_postgis': True,
                         'with_devel': True,
                         'extensions': ['hstore']}
        provision_database(backend_options=backend_options)


class AOLDeployer(DjangoDeployer):
    """
    TBD
    """


@command
def deploy_app(rebuild=True):
    deploy(AOLDeployer, rebuild=rebuild)
