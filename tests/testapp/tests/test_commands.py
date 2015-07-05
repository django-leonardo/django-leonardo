
from __future__ import absolute_import, unicode_literals

import os
from django.test import TestCase

from django.core import management


class ManagementCommandsTest(TestCase):

    def test_01_sync_all(self):

        try:
            # fix sqlite
            from django.db import connection
            connection.cursor()
            connection.connection.text_factory = lambda x: unicode(x, "utf-8", "ignore")
        except Exception:
            pass

        management.call_command('sync_all', force=True)

    def test_02_rebuild_index(self):

        management.call_command('rebuild_index', interactive=False)

    def test_03_import_files(self):
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)),)
        management.call_command('import_files', path=path)

    """
    in this time is not testable because sqlite hasn't themes
    def test_bootstrap_site(self):
        management.call_command('bootstrap_site',
                                    url='http://github.com/django-leonardo/django-leonardo/raw/develop/contrib/bootstrap/demo.yaml',
                                    sync= True)
        management.call_command('bootstrap_site',
                                options={
                                    'url': 'http://github.com/django-leonardo/django-leonardo/raw/develop/contrib/bootstrap/blog.yaml',
                                    'sync': False,
                                    })
    """
