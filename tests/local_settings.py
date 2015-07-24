from __future__ import absolute_import, unicode_literals

import sys
import os

SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'memory:',
        'TEST_NAME': 'test_db:',
    }
}

try:
    import mysql  # noqa
except Exception:
    pass
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'django_leonardo',
            'USER': 'travis',
        }
    }

MIGRATION_MODULES = {
    'web': 'notmigrations',
    'media': 'notmigrations',
}


try:
    import psycopg2  # noqa
except Exception as e:
    pass
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'django_leonardo',
            'USER': 'postgres',
        }
    }
    # monkeypath postgres tests
    MIGRATION_MODULES['dbtemplates'] = 'notmigrations'
    MIGRATION_MODULES['sites'] = 'notmigrations'
    MIGRATION_MODULES['contenttypes'] = 'notmigrations'
    MIGRATION_MODULES['auth'] = 'notmigrations'
    MIGRATION_MODULES['reversion'] = 'notmigrations'

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
BASEDIR = os.path.dirname(__file__)
MEDIA_ROOT = os.path.join(BASEDIR, 'media/')
STATIC_ROOT = os.path.join(BASEDIR, 'static/')
SECRET_KEY = 'supersikret'
USE_TZ = True

ROOT_URLCONF = 'testapp.urls'
LANGUAGES = (('en', 'English'), ('cs', 'Czech'))

LEONARDO_MODULE_AUTO_INCLUDE = False

APPS = [
    'testapp',
    'leaonrdo_theme_bootswatch',
]
