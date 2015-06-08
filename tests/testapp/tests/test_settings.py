
from __future__ import absolute_import, unicode_literals

from django.test import TestCase
from django.conf import settings
from leonardo.base import leonardo
from leonardo.module import web


class SettingsBaseTest(TestCase):

    def test_01_simple_settings_key(self):
        self.assertEqual(settings.APP_SPECIFIC_SETTINGS, True)

    def test_02_custom_apps_with_defaults(self):
        contains = False
        if 'leonardo.module.media' in settings.INSTALLED_APPS:
            contains = True
        self.assertEqual(contains, True)

    def test_get_app_modules(self):
        self.assertEqual(settings._APPS[1], web)

    def test_live_config(self):
        from constance import config
        self.assertEqual(
            getattr(config, 'GOOGLE_ANALYTICS_SITE_SPEED'), False)
