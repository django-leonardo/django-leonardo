
#!/usr/bin/env python
import os
import sys

import django
from django.core.management import execute_from_command_line

possible_topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                                os.pardir,
                                                os.pardir,
                                                os.pardir))


if os.path.exists(os.path.join(possible_topdir, 'leonardo', '__init__.py')):
    sys.path.insert(0, possible_topdir)
    sys.path.insert(0, os.path.normpath(os.path.join(possible_topdir, os.pardir)))

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'leonardo.settings'
    django.setup()
    execute_from_command_line(sys.argv)
