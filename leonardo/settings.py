
from __future__ import absolute_import

import os
from os.path import abspath, dirname, join, normpath

import django
import six
from distutils.version import StrictVersion
from leonardo import default, merge

from .base import leonardo

EMAIL = {
    'HOST': 'mail.domain.com',
    'PORT': '25',
    'USER': 'username',
    'PASSWORD': 'pwd',
    'SECURITY': True,
}

RAVEN_CONFIG = {}

ALLOWED_HOSTS = ['*']

USE_TZ = True

DEBUG = True

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('admin', 'mail@leonardo.cz'),
)

DEFAULT_CHARSET = 'utf-8'

MANAGERS = ADMINS

SITE_ID = 1

SITE_NAME = 'hrcms'

TIME_ZONE = 'Europe/Prague'

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('cs', 'CS'),
    ('en', 'EN'),
)

USE_I18N = True

# SOME DEFAULTS
MEDIA_ROOT = '/srv/leonardo/sites/demo/media/'
STATIC_ROOT = '/srv/leonardo/sites/demo/static/'

MEDIA_URL = '/media/'
STATIC_URL = '/static/'


"""
try to support old Django
"""

TEMPLATE_LOADERS = (
    'dbtemplates.loader.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'horizon.loaders.TemplateLoader',
)

if StrictVersion(django.get_version()) > StrictVersion('1.7.7'):

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), 'templates')
            ],
            'OPTIONS': {
                'context_processors': default.context_processors,
                'loaders': [
                    'dbtemplates.loader.Loader',
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    'horizon.loaders.TemplateLoader',
                ]
            },
        },
    ]

else:

    TEMPLATE_DIRS = [
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'templates')
    ]

    TEMPLATE_CONTEXT_PROCESSORS = default.context_processors


DBTEMPLATES_USE_REVERSION = True

DBTEMPLATES_MEDIA_PREFIX = '/static-/'

DBTEMPLATES_USE_CODEMIRROR = False

DBTEMPLATES_USE_TINYMCE = False

DBTEMPLATES_AUTO_POPULATE_CONTENT = True

DBTEMPLATES_ADD_DEFAULT_SITE = True

FILER_ENABLE_PERMISSIONS = True  # noqa

MIDDLEWARE_CLASSES = default.middlewares

ROOT_URLCONF = 'leonardo.urls'

MARKITUP_FILTER = ('markitup.renderers.render_rest', {'safe_mode': True})

INSTALLED_APPS = default.apps

# For easy_thumbnails to support retina displays (recent MacBooks, iOS)

FEINCMS_USE_PAGE_ADMIN = False

LEONARDO_USE_PAGE_ADMIN = True

FEINCMS_DEFAULT_PAGE_MODEL = 'web.Page'

##########################


STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    'compressor.finders.CompressorFinder',
)

LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_URL = "/"

REDACTOR_OPTIONS = {'lang': 'en', 'plugins': [
    'table', 'video', 'fullscreen', 'fontcolor', 'textdirection']}
REDACTOR_UPLOAD = 'uploads/'

LOGOUT_ON_GET = True

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

# migrations support
MIGRATION_MODULES = {
    'filer': 'filer.migrations_django',
}

CRISPY_TEMPLATE_PACK = 'bootstrap'

SECRET_KEY = None

APPS = []

try:
    # full settings
    from leonardo_site.local.settings import *
except ImportError:
    pass

try:
    # local settings
    from local_settings import *
except ImportError:
    pass

REVERSION_MIDDLEWARE = [
    'reversion.middleware.RevisionMiddleware']


OAUTH_CTP = [
    "allauth.socialaccount.context_processors.socialaccount"
]

APPS = merge(APPS, default.core)

if 'media' in APPS:
    FILER_IMAGE_MODEL = 'leonardo.module.media.models.Image'

try:
    from leonardo.conf.horizon import *
    from leonardo.conf.static import *
except Exception, e:
    pass


APPLICATION_CHOICES = []


def elephantblog_entry_url_app(self):
    from leonardo.module.web.widget.application.reverse import app_reverse
    return app_reverse(
        'elephantblog_entry_detail',
        'elephantblog.urls',
        kwargs={
            'year': self.published_on.strftime('%Y'),
            'month': self.published_on.strftime('%m'),
            'day': self.published_on.strftime('%d'),
            'slug': self.slug,
        })


def elephantblog_categorytranslation_url_app(self):
    from leonardo.module.web.widget.application.reverse import app_reverse
    return app_reverse(
        'elephantblog_category_detail',
        'elephantblog.urls',
        kwargs={
            'slug': self.slug,
        })


def oscar_product_url_app(self):
    from leonardo.module.web.widget.application.reverse import app_reverse
    return app_reverse(
        'detail',
        'leonardo_module_eshop.apps.catalog',
        kwargs={'product_slug': self.slug, 'pk': self.id})

ABSOLUTE_URL_OVERRIDES = {
    'catalogue.product': oscar_product_url_app,
    'elephantblog.entry': elephantblog_entry_url_app,
    'elephantblog.categorytranslation':
    elephantblog_categorytranslation_url_app,
}

try:

    # override settings
    try:
        from leonardo_site.conf.feincms import *
    except ImportError:
        pass

    from django.utils.importlib import import_module  # noqa

    from django.utils.module_loading import module_has_submodule  # noqa

    widgets = {}

    for app, mod in six.iteritems(leonardo.get_app_modules(APPS)):

        # load all settings key
        if module_has_submodule(mod, "settings"):
            try:
                settings_mod = import_module(
                    '{0}.settings'.format(mod.__name__))
                for k in dir(settings_mod):
                    if not k.startswith("_"):
                        val = getattr(settings_mod, k, None)
                        globals()[k] = val
                        locals()[k] = val
            except Exception as e:
                pass

        if hasattr(mod, 'default'):

            APPLICATION_CHOICES = merge(APPLICATION_CHOICES, getattr(
                mod.default, 'plugins', []))

            INSTALLED_APPS = merge(
                INSTALLED_APPS, getattr(mod.default, 'apps', []))

            MIDDLEWARE_CLASSES = merge(
                MIDDLEWARE_CLASSES, getattr(
                    mod.default, 'middlewares', []))
            AUTHENTICATION_BACKENDS = merge(
                AUTHENTICATION_BACKENDS, getattr(
                    mod.default, 'auth_backends', []))

            if StrictVersion(django.get_version()) > StrictVersion('1.7.7'):
                TEMPLATES[0]['DIRS'] = merge(TEMPLATES[0]['DIRS'], getattr(
                    mod.default, 'dirs', []))
                cp = TEMPLATES[0]['OPTIONS']['context_processors']
                TEMPLATES[0]['OPTIONS']['context_processors'] = merge(
                    cp, getattr(mod.default, 'context_processors', []))

            else:

                TEMPLATE_CONTEXT_PROCESSORS = merge(
                    TEMPLATE_CONTEXT_PROCESSORS, getattr(
                        mod.default, 'context_processors', []))
                TEMPLATE_DIRS = merge(
                    TEMPLATE_DIRS, getattr(
                        mod.default, 'dirs', []))

            # collect grouped widgets
            widgets[getattr(mod.default, 'optgroup', app.capitalize())] = \
                getattr(mod.default, 'widgets', [])

    from leonardo.module.web.models import Page
    from leonardo.module.web.widget import ApplicationWidget

    # register external apps
    Page.create_content_type(
        ApplicationWidget, APPLICATIONS=APPLICATION_CHOICES)

    # register widgets
    for optgroup, _widgets in six.iteritems(widgets):
        for widget in _widgets:
            Page.create_content_type(widget, optgroup=optgroup)

    Page.register_extensions(*PAGE_EXTENSIONS)
    Page.register_default_processors(LEONARDO_FRONTEND_EDITING)
except Exception as e:
    raise e

if not SECRET_KEY:
    try:
        LOCAL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  'local')

        from horizon.utils import secret_key

        SECRET_KEY = secret_key.generate_or_read_from_file(os.path.join(LOCAL_PATH,
                                                                        '.secret_key_store'))
    except Exception:
        pass


# enable reversion for every req
if 'reversion' in INSTALLED_APPS:
    MIDDLEWARE_CLASSES = merge(REVERSION_MIDDLEWARE, MIDDLEWARE_CLASSES)

# FINALLY OVERRIDE ALL

try:
    # local settings
    from local_settings import *
except ImportError:
    pass

try:
    # full settings
    from project.local.settings import *
except ImportError:
    pass

# and again merge core with others
APPS = merge(APPS, default.core)

# ensure if bootstra_admin is on top of INSTALLED_APPS
if 'bootstrap_admin' in INSTALLED_APPS:
    BOOTSTRAP_ADMIN_SIDEBAR_MENU = True
    # INSTALLED_APPS.remove('bootstrap_admin')
    #INSTALLED_APPS = ['bootstrap_admin'] + INSTALLED_APPS
