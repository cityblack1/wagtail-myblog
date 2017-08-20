from __future__ import absolute_import, unicode_literals

from .base import *

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.cityblack1.cc']

try:
    from .local import *
except ImportError:
    pass
