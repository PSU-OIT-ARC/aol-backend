from setuptools import setup, find_packages


VERSION = '1.3.3'


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
        'django>=1.8.13,<1.9',
        'ldap3<2.0',
        'django-arcutils[ldap]>=2.11.1',
        'django-bootstrap-form>=3.2.1',
        'django-local-settings>=1.0a20',
        'django-pgcli>=0.0.2',
        'Pillow>=3.3.0',
        'psycopg2>=2.6.2',
        'pyshp>=1.2.3',
        'pytz>=2016.4',
        'requests>=2.10.0',
        'Shapely>=1.5.16',
	'raven>=5.31.0',
    ],
    extras_require={
        'dev': [
            'psu.oit.arc.tasks',
            'flake8',
            'mock',
            'model_mommy',
            'mommy_spatial_generators',
        ]
    },
)
