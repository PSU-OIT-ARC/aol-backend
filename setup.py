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
        'psu.oit.wdt.emcee>=1.0.0.rc2',
        'django>=1.8.18,<1.9',
        'django-arcutils[ldap]>=2.24',
        'django-bootstrap-form>=3.2.1',
        'django-pgcli>=0.0.2',
        'Pillow>=4.3.0',
        'psycopg2>=2.7.3.1',
        'pyshp>=1.2.12',
        'pytz>=2017.2',
        'requests>=2.18.4',
        'Shapely>=1.6.1',
        'raven>=6.2.1',
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
