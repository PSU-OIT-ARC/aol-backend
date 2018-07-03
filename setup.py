from setuptools import setup, find_packages


VERSION = '1.4.0.dev0'


setup(
    name='psu.oit.arc.aol',
    version=VERSION,
    description='Atlas of Oregon Lakes',
    author='PSU - OIT - ARC',
    author_email='consultants@pdx.edu',
    url='http://aol.research.pdx.edu/',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'psu.oit.wdt.emcee>=1.0.0.rc7,<1.1',
        'django~=1.11.14',
        'django-arcutils[ldap]~=2.24',
        'django-bootstrap-form~=3.4',
        'django-pgcli~=0.0.2',

        'requests~=2.19.1',
        'Pillow~=5.2.0',
        'psycopg2~=2.7.5',
        'pyshp~=1.2.12',
        'pytz~=2018.3',
        'Shapely~=1.6.4',
        'raven~=6.9.0',
    ],
    extras_require={
        'dev': [
            'flake8',
            'mock',
            'model_mommy',
            'mommy_spatial_generators',
            'docker-compose'
        ]
    },
)
