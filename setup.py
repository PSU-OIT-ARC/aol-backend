# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import sys
import re
import os

if sys.version_info < (3, 6):
    raise Exception('AOL requires Python versions 3.6 or later.')


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
        'pytz',
        'dateparser~=1.0.0',
        'beautifulsoup4~=4.9.3',
        'requests~=2.25.1',
        'Pillow~=8.1.1',
        'psycopg2~=2.8.6',
        'pyshp~=2.1.3',
        'Shapely~=1.7.1',
        'uritemplate~=3.0.1',
        'psu.oit.wdt.emcee[aws]~=1.1.0.b4',
        'django~=2.2.19',
        'djangorestframework~=3.12.4',
        'celery~=5.0.5',
        'django-filter~=2.4.0',
        'social-auth-core~=4.1.0',
        'social-auth-app-django~=4.0.0',
        'django-ckeditor~=6.0.0',
        'sentry-sdk~=1.0.0',
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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
