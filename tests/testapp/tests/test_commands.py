
from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from django.core import management


class ManagementCommandsTest(TestCase):
    def test_01_sync_all(self):
        management.call_command('sync_all')
