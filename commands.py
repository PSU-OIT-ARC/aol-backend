import os.path

from emcee.runner.config import YAMLCommandConfiguration
from emcee.runner import command, configs, config
from emcee.runner.commands import remote
from emcee.runner.utils import confirm
from emcee.app.config import YAMLAppConfiguration

from emcee.commands.transport import warmup
from emcee.commands.files import copy_file
from emcee.commands.deploy import deploy, list_builds
from emcee.commands.python import virtualenv, install
from emcee.commands.django import manage

from emcee.provision.base import provision_host, patch_host
from emcee.provision.python import provision_python, provision_uwsgi
from emcee.provision.gis import provision_gis
from emcee.provision.services import (provision_nginx,
                                      provision_supervisor,
                                      provision_rabbitmq)
from emcee.provision.secrets import provision_secret, show_secret

from emcee.deploy import deployer
from emcee.deploy.services import (push_crontab,
                                   push_supervisor_config,
                                   restart_supervisor)
from emcee.deploy.python import push_uwsgi_config, restart_uwsgi
from emcee.deploy.django import LocalProcessor, Deployer

from emcee.backends.aws.infrastructure.commands import *
from emcee.backends.aws.provision.db import (provision_database,
                                             archive_database,
                                             restore_database,
                                             update_database_ca,
                                             update_database_client)
from emcee.backends.aws.provision.volumes import (provision_volume,
                                                  provision_swapfile)
from emcee.backends.aws.deploy import EC2RemoteProcessor


configs.load(YAMLCommandConfiguration)


@command
def provision(createdb=False):
    # Configure host properties and prepare host platforms
    provision_host()
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
        provision_database(backend_options={'with_postgis': True,
                                            'extensions': ['hstore']})

    # Provision application secrets
    client_id = input("Enter the ArcGIS Client ID: ")
    provision_secret('ArcGISClientID', client_id)
    client_secret = input("Enter the ArcGIS Client Secret: ")
    provision_secret('ArcGISClientSecret', client_secret)
    oauth_secret = input("Enter the Google OAuth secret: ")
    provision_secret('GoogleOAuth2Secret', oauth_secret)


@command
def provision_media_assets():
    # Create media directory on EBS mount and link to app's media root
    printer.header("Creating media directory on EBS volume...")
    remote(('mkdir', '-p', '/vol/store/media'), sudo=True)
    remote(('test', '-h', config.remote.path.media, '||',
            'ln', '-sf', '/vol/store/media', config.remote.path.media), sudo=True)

    # Set the correct permissions on generated assets
    printer.header("Setting permissions on media assets...")
    owner = '{}:{}'.format(config.iam.user, config.services.nginx.group)
    remote(('chown', '-R', owner, '/vol/store/media'), sudo=True)
    remote(('chown', '-R', owner, config.remote.path.media), sudo=True)

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


class AOLRemoteProcessor(EC2RemoteProcessor):
    def activate_application(self, archive_path):
        super().activate_application(archive_path)

        # Reload the supervisor process
        restart_supervisor()


@deployer()
class AOLDeployer(Deployer):
    local_processor_cls = LocalProcessor
    remote_processor_cls = AOLRemoteProcessor
    app_config_cls = YAMLAppConfiguration

    def setup_application_hosting(self):
        super().setup_application_hosting()

        # Install crontab
        push_crontab(template='assets/crontab')

        # Install supervisor worker configuration
        push_supervisor_config(template='assets/supervisor.conf')
