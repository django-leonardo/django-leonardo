
from __future__ import absolute_import, unicode_literals

from django.test import TestCase
from leonardo import settings

class SettingsBaseTest(TestCase):
    def test_01_simple_settings_key(self):
        self.assertEqual(settings.APP_SPECIFIC_SETTINGS, True)
