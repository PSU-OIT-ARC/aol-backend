"""The Atlas of Oregon Lakes."""
import sys

if sys.version_info[0] == 3 and sys.version_info < (3, 6):
    raise Exception('ORO requires Python version 3.6 or later.')


__version__ = '1.5.6'
__author__ = 'OIT Web & Mobile Team, Portland State University'
__homepage__ = 'https://aol.research.pdx.edu'

__all__ = ['__version__']
