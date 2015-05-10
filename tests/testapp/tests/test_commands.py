
from __future__ import absolute_import, unicode_literals

import os
from django.test import TestCase

from django.core import management


class ManagementCommandsTest(TestCase):

    def test_01_sync_all(self):

        # fix sqlite
        from django.db import connection
        connection.cursor()
        connection.connection.text_factory = lambda x: unicode(x, "utf-8", "ignore")

        management.call_command('sync_all', force=True)

    def test_02_rebuild_index(self):

        management.call_command('rebuild_index', interactive=False)

    def test_03_import_files(self):
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)),)
        management.call_command('import_files', path=path)
