from emcee.runner.config import YAMLCommandConfiguration
from emcee.runner import command, configs, config
from emcee.runner.commands import remote
from emcee.runner.utils import confirm
from emcee.app.config import LegacyAppConfiguration
from emcee.app import app_configs
from emcee import printer

from emcee.commands.db import pg_dump, pg_restore
from emcee.commands.deploy import deploy
from emcee.commands.python import virtualenv, install
from emcee.commands.django import manage, manage_remote
from emcee.commands.files import copy_file

from emcee.provision.base import provision_host, patch_host
from emcee.provision.python import provision_python
from emcee.provision.gis import provision_gis
from emcee.provision.services import (provision_nginx,
                                      provision_supervisor,
                                      provision_rabbitmq)
from emcee.provision.secrets import provision_secret, show_secret

from emcee.deploy.utils import copy_file_local
from emcee.deploy.base import push_crontab, push_supervisor_config
from emcee.deploy.python import push_uwsgi_config, restart_uwsgi
from emcee.deploy.django import LocalProcessor, Deployer

from emcee.backends.aws.infrastructure.commands import *
from emcee.backends.aws.provision.db import (provision_database,
                                             import_database,
                                             update_database_ca,
                                             update_database_client)
from emcee.backends.aws.provision.volumes import (provision_volume,
                                                  provision_swapfile)
from emcee.backends.aws.deploy import EC2RemoteProcessor


configs.load('default', 'commands.yml', YAMLCommandConfiguration)
# app_configs.load('default', LegacyAppConfiguration)


@command
def provision_app(createdb=False):
    # Configure host properties and prepare host platforms
    provision_host(initialize_host=True)
    provision_python()
    provision_gis()
    provision_uwsgi()

    # Provision application services
    provision_nginx()
    provision_supervisor()
    provision_rabbitmq()

    # Initialize/prepare attached EBS volume
    provision_volume(mount_point='/vol/store', filesystem='ext4')

    # Initialize swapfile on EBS volume
    provision_swapfile(1024, path='/vol/store')

    # Provision database dependencies
    update_database_client('postgresql', with_devel=True)
    update_database_ca('postgresql')
    if createdb:
        provision_database(with_postgis=True,
                           extensions=['hstore'])

    # Provision application secrets
    client_id = input("Enter the ArcGIS Client ID: ")
    provision_secret('ArcGISClientID', client_id)
    client_secret = input("Enter the ArcGIS Client Secret: ")
    provision_secret('ArcGISClientSecret', client_secret)
    oauth_secret = input("Enter the Google OAuth secret: ")
    provision_secret('GoogleOAuth2Secret', oauth_secret)


@command
def provision_media_assets():
    app_media_root = os.path.join(config.remote.path.root, 'media')
    owner = '{}:{}'.format(config.iam.user, config.remote.nginx.group)

    # Create media directory on EBS mount and link to app's media root
    remote(('mkdir', '-p', '/vol/store/media'), sudo=True)
    remote(('mkdir', '-p', app_media_root), sudo=True)
    remote(('test', '-h', config.remote.path.media, '||',
            'ln', '-sf', '/vol/store/media', config.remote.path.media), sudo=True)

    # Set the correct permissions on generated assets
    remote(('chown', '-R', owner, '/vol/store/media'), sudo=True)
    remote(('chown', '-R', owner, app_media_root), sudo=True)

    # Synchronize icons and assorted media assets:
    archive_path = 'media.tar'
    if os.path.exists(archive_path):
        if not confirm("Synchronize media from '{}'?".format(archive_path)):
            return

        copy_file(archive_path, config.remote.path.media)
        remote(('tar', 'xvf', archive_path, '&&',
                'rm', archive_path),
               cd=config.remote.path.media
        )


class AOLLocalProcessor(LocalProcessor):
    def make_dists(self):
        """
        Handles preparation of the environment-specific settings module
        as this project utilizes pure-python configuration and does not
        engage built-in support in Emcee to manage app configuration.
        """
        copy_file_local('aol/settings/{}.py'.format(config.env),
                        'aol/settings/current.py')

        super(AOLLocalProcessor, self).make_dists()


class AOLDeployer(Deployer):
    """
    TBD
    """
    local_processor_cls = AOLLocalProcessor
    remote_processor_cls = EC2RemoteProcessor

    def bootstrap_application(self):
        super().bootstrap_application()

        # Install crontab
        push_crontab(template='assets/crontab')

    def setup_application_hosting(self):
        super().setup_application_hosting()

        # Install supervisor worker configuration
        push_supervisor_config(template='assets/supervisor.conf')


@command
def deploy_app(rebuild=True):
    deploy(AOLDeployer, rebuild=rebuild)
