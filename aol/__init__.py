"""The Atlas of Oregon Lakes."""
import sys

if sys.version_info < (3, 7):
    raise Exception('ORO requires Python version 3.7 or later.')


__version__ = '1.6.4'
__author__ = 'OIT Web & Mobile Team, Portland State University'
__homepage__ = 'https://psu-arc-oit.github.io/aol-backend'

__all__ = ['__version__']
