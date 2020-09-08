#!/usr/bin/env python
import os
import sys
from os.path import abspath, dirname, join, normpath

import django
from django.core.management import execute_from_command_line

sys.path.append('/app/site')
sys.path.append('/app/module')
sys.path.append('/app/settings')

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'leonardo.settings'
    django.setup()
    execute_from_command_line(sys.argv)
