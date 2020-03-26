# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import sys
import re
import os

if sys.version_info < (3, 5):
    raise Exception('AOL requires Python versions 3.5 or later.')


def get_requirements():
    with open('requirements.txt', 'r') as requirements:
        return [line.strip()
                for line in requirements
                if line and \
                not line.startswith('#') and \
                not line.startswith('--')]

# Metadata extraction by parsing 'aol' module directly.
#   https://github.com/celery/kombu/blob/master/setup.py
re_meta = re.compile(r'__(\w+?)__\s*=\s*(.*)')
re_doc = re.compile(r'^"""(.+?)"""')

def add_default(m):
    attr_name, attr_value = m.groups()
    return ((attr_name, attr_value.strip("\"'")),)

def add_doc(m):
    return (('doc', m.groups()[0]),)

pats = {re_meta: add_default, re_doc: add_doc}
here = os.path.abspath(os.path.dirname(__file__))
meta_fh = open(os.path.join(here, 'aol/__init__.py'))

try:
    meta = {}
    for line in meta_fh:
        if line.strip() == '# -eof meta-':
            break
        for pattern, handler in pats.items():
            m = pattern.match(line.strip())
            if m:
                meta.update(handler(m))
finally:
    meta_fh.close()

setup(
    name='psu.oit.arc.aol',
    version=meta['version'],
    description=meta['doc'],
    author=meta['author'],
    long_description=open('README.md').read(),
    url=meta['homepage'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'pytz~=2019.3',
        'dateparser~=0.7.2',
        'beautifulsoup4~=4.8.1',
        'requests~=2.22.0',
        'Pillow~=7.0.0',
        'psycopg2~=2.8.4',
        'pyshp~=2.1.0',
        'Shapely~=1.7.0',
        'uritemplate~=3.0.0',
        'psu.oit.wdt.emcee~=1.0.4',
        'django~=2.2.10',
        'djangorestframework~=3.11.0',
        'celery~=4.4.0',
        'django-filter~=2.2.0',
        'social-auth-core~=3.2.0',
        'social-auth-app-django~=3.1.0',
        'django-ckeditor~=5.9.0',
        'sentry-sdk~=0.14.1',
    ],
    extras_require={
        'dev': [
            'flake8',
            'mock',
            'model_mommy',
            'docker-compose',
            'django-cors-middleware'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable'
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
