#!/usr/bin/env python
from __future__ import absolute_import, unicode_literals

import os
import sys


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings.dev")

from django.core.management import execute_from_command_line

execute_from_command_line(['runserver'])
