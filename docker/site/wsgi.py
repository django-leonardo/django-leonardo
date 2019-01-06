#!/usr/bin/env python

import os
import sys
from os.path import abspath, dirname, join, normpath

import django
import django.core.handlers.wsgi
from django.core.management import execute_from_command_line

sys.path.append('/app/site')
sys.path.append('/app/module')
sys.path.append('/app/settings')

os.environ['DJANGO_SETTINGS_MODULE'] = 'leonardo.settings'
django.setup()

application = django.core.handlers.wsgi.WSGIHandler()
