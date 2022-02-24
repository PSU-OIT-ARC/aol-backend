# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import sys
import re
import os

if sys.version_info < (3, 7):
    raise Exception('AOL requires Python versions 3.7 or later.')


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
        'dateparser~=1.1.0',
        'beautifulsoup4~=4.10.0',
        'requests~=2.27.0',
        'Pillow~=9.0.0',
        'psycopg2~=2.9.0',
        'pyshp~=2.2.0',
        'Shapely~=1.8.0',
        'uritemplate~=4.1.0',
        'psu.oit.wdt.emcee[aws]~=1.1.0',
        'django~=3.2.0',
        'djangorestframework~=3.13.0',
        'celery~=5.2.0',
        'uwsgi~=2.0.0',
        'django-filter~=21.0',
        'social-auth-core~=4.2.0',
        'social-auth-app-django~=5.0.0',
        'django-ckeditor~=6.2.0',
        'sentry-sdk~=1.5.0',
        'django-sendfile2~=0.6.0',
        'django-robots~=5.0',
    ],
    extras_require={
        'dev': [
            'flake8',
            'mock',
            'model_mommy',
            'docker-compose',
            'django-cors-headers'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable'
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
