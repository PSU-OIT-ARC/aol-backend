from setuptools import setup, find_packages


VERSION = '1.3.0.dev0'


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
        'django>=1.8.11,<1.9',
        'django-arcutils[ldap]>=2.8.0',
        'django-bootstrap-form>=3.2',
        'django-local-settings>=1.0a17',
        'django_pgcli>=0.0.2',
        'Pillow>=3.1.1',
        'psycopg2>=2.6.1',
        'pyshp>=1.2.3',
        'pytz>=2016.2',
        'Shapely>=1.5.13',
        'requests>=2.9.1',
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
