#!/usr/bin/env python
import os
import sys
from os.path import join

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "leonardo.settings")
    sys.path.insert(
        0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from django.core.management import execute_from_command_line
    import django
    django.setup()
    execute_from_command_line(sys.argv)
