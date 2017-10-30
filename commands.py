from runcommands import command

from emcee.commands.javascript import npm_install
from emcee.commands.python import virtualenv, install
from emcee.commands.django import manage
from emcee.commands.deploy import deploy

from emcee.backends.dev.db import provision_database as provision_database_local
from emcee.backends.aws.provision.python import provision_python
from emcee.backends.aws.provision.services.local import provision_nginx
from emcee.backends.aws.provision.services.remote import provision_database
from emcee.backends.aws.deploy import AWSPythonDeployer
from emcee.backends.aws.infrastructure.commands import *


@command(env='dev', timed=True)
def init(config, overwrite=False, drop_db=False):
    virtualenv(config, config.venv, overwrite=overwrite)
    install(config)
    npm_install(config)
    # provision_database_local(config, drop=drop_db, with_postgis=True)
    manage(config, 'migrate --noinput')


@command(env=True)
def deploy_app(config, provision=False, createdb=False):
    if provision:
        provision_python(config)
        provision_nginx(config, with_gis=True)
    if createdb:
        provision_db(config, with_postgis=True,
                     extensions=['postgis', 'hstore'])

    deploy(config, deployer_class=AWSPythonDeployer)
