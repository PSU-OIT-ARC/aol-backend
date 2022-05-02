import oyaml
import sys
import io

IMAGE_BASENAME = 'ghcr.io/psu-oit-arc/aol-backend'
ENVIRONMENTS = ['prod', 'stage']
CONFIGS = [
    'docker-compose.{}.yml',
    '{}.yml',
    '{}-bootstrap.yml'
]


def update_config(config, env, version):
    path = config.format(env)
    updated = False
    obj = None

    with io.open(path, 'r') as f:
        obj = oyaml.safe_load(f)
        if 'services' not in obj:
            print("No services listed in '{}'".format(path))
            return

        for _, service in obj['services'].items():
            for k, v in service.items():
                if k == 'image' and v.startswith(IMAGE_BASENAME):
                    service['image'] = ':'.join([v.split(':')[0], version])
                    updated = True

    if not updated:
        print("No service images modified.")
        return

    with io.open(path, 'w') as f:
        oyaml.safe_dump(obj, stream=f)


if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("Usage: bump_version.py")
        sys.exit(1)

    from aol import __version__
    for env in ENVIRONMENTS:
        for config in CONFIGS:
            update_config(config, env, __version__)
