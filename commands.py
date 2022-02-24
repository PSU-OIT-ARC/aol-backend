import os.path
import time

from emcee.runner.config import YAMLCommandConfiguration
from emcee.runner import command, configs, config
from emcee.runner.commands import remote
from emcee.runner.utils import confirm
from emcee.app.config import YAMLAppConfiguration
from emcee import printer

from emcee.commands.transport import warmup, shell
from emcee.commands.files import copy_file
from emcee.commands.deploy import deploy, list_builds

from emcee.provision.base import provision_host, patch_host
from emcee.provision.docker import provision_docker, authenticate_ghcr
from emcee.provision.secrets import provision_secret, show_secret

from emcee.deploy.docker import publish_images
from emcee.deploy import deployer, docker

from emcee.backends.aws.infrastructure.commands import *
from emcee.backends.aws.provision.db import (provision_database,
                                             archive_database,
                                             restore_database,
                                             update_database_ca,
                                             update_database_client)
from emcee.backends.aws.provision.volumes import (provision_volume,
                                                  provision_swapfile)

configs.load(YAMLCommandConfiguration)


@command
def provision(createdb=False):
    # Configure host properties and prepare host platforms
    provision_host()

    # Provision application services
    provision_docker()

    # Provision containers volumes
    printer.header("Initializing container volumes...")
    for service in ['rabbitmq']:
        services_path = os.path.join(config.remote.path.root, 'services', service)
        remote(('mkdir', '-p', services_path), run_as=config.iam.user)

    # Initialize/prepare attached EBS volume
    provision_volume(mount_point='/vol/store', filesystem='ext4')

    # Initialize swapfile on EBS volume
    provision_swapfile(1024, path='/vol/store')

    # Create persistent asset directory on EBS mount
    printer.header("Creating media directory on EBS volume...")
    remote(('mkdir', '-p', '/vol/store/media'), sudo=True)

    # Create link for log storage path
    printer.header("Creating log path...")
    remote(('test', '-h', config.remote.path.log_dir, '||',
            'mkdir', '-p', config.remote.path.log_dir))

    # Create link for static asset path
    printer.header("Creating static asset path...")
    remote(('test', '-h', config.remote.path.static, '||',
            'mkdir', '-p', config.remote.path.static))

    # Create link for stored media path
    remote(('test', '-h', config.remote.path.media, '||',
            'ln', '-sf', '/vol/store/media', config.remote.path.media))

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

    # Set the correct permissions on generated assets
    printer.header("Setting permissions on media assets...")
    owner = '{}:{}'.format(config.iam.user, config.services.nginx.group)
    remote(('chown', '-h', owner, config.remote.path.media), sudo=True)
    remote(('chown', '-R', owner, '/vol/store/media'), sudo=True)

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

    # Authenticates appropriate user on remote host for
    # interaction with the GitHub Container Registry.
    authenticate_ghcr()


@command
def maintenance_mode():
    printer.info("Activating application maintenance mode...")
    remote_processor = AOLRemoteProcessor(options=None)

    # remove user-facing services from stack
    if remote_processor.remove_stack_services(AOL_SERVICES['frontend']):
        # wait a predetermined about of time for the
        # task queues to be emptied of work
        printer.info("Waiting 60s for task queue to empty...")
        time.sleep(60)

    # remove the remaining services from stack
    remote_processor.remove_stack_services(AOL_SERVICES['backend'])


class AOLLocalProcessor(docker.LocalProcessor):
    include_app = True
    include_uwsgi = True
    include_nginx = True


class AOLRemoteProcessor(docker.RemoteProcessor):
    """
    TBD
    """


@deployer()
class AOLDeployer(docker.Deployer):
    local_processor_cls = AOLLocalProcessor
    remote_processor_cls = AOLRemoteProcessor
    app_config_cls = YAMLAppConfiguration

    def bootstrap_application(self):
        if not self.remote_processor.is_stack_active():
            printer.error("Stack is not active in remote environment.")
            return

        # Enable maintenance mode before bootstrapping application
        maintenance_mode()

        printer.info("Bootstrapping application...")
        bootstrap_stackfile = '{}-bootstrap.yml'.format(config.env)
        self.remote_processor.deploy_stack(stackfile=bootstrap_stackfile)

        # force bootstrap service to run
        self.remote_processor.scale_stack_service('bootstrap', 1, wait=True)
        self.remote_processor.scale_stack_service('bootstrap', 0)

        # force update check for all service images not uniquely tagged/versioned
        self.remote_processor.pull_stack_images()


AOL_SERVICES = {}
AOL_SERVICES['frontend'] = [
    'scheduler', 'app'
]
AOL_SERVICES['backend'] = [
    'celery'
]
