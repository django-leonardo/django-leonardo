#!/usr/bin/env python

import os
import sys

import django
from django.core.management import execute_from_command_line
from django.core.wsgi import get_wsgi_application

possible_topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                                os.pardir,
                                                os.pardir,
                                                os.pardir))


if os.path.exists(os.path.join(possible_topdir, 'leonardo', '__init__.py')):
    sys.path.insert(0, possible_topdir)
    sys.path.insert(0, os.path.normpath(
        os.path.join(possible_topdir, os.pardir)))

os.environ['DJANGO_SETTINGS_MODULE'] = 'leonardo.settings'
django.setup()

application = get_wsgi_application()
