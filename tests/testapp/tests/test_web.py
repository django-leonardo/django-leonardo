
from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from leonardo.module.web.models import Page
from leonardo.module.web import default


class WebBaseTest(TestCase):
    def test_01_simple_content_type_creation(self):
        for widget in default.widgets:
            self.assertIsNotNone(Page.content_type_for(widget))
