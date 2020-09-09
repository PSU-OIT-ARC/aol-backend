"""The Atlas of Oregon Lakes."""
import sys

if sys.version_info[0] == 3 and sys.version_info < (3, 5):
    raise Exception('ORO requires Python version 3.5 or later.')


__version__ = '1.5.2'
__author__ = 'OIT Web & Mobile Team, Portland State University'
__homepage__ = 'https://aol.research.pdx.edu'

__all__ = ['__version__']
