
from __future__ import absolute_import

import os
from os.path import abspath, dirname, join, normpath

from oscar import OSCAR_MAIN_TEMPLATE_DIR

from leonardo import default, merge

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 120,
        'KEY_PREFIX': 'CACHE_HRCMS'
    }
}

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

TEMPLATE_CONTEXT_PROCESSORS = default.ctp

TEMPLATE_LOADERS = (
    'dbtemplates.loader.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'horizon.loaders.TemplateLoader',
)

DBTEMPLATES_USE_REVERSION = True

DBTEMPLATES_MEDIA_PREFIX = '/static-/'

DBTEMPLATES_USE_CODEMIRROR = False

DBTEMPLATES_USE_TINYMCE = False

DBTEMPLATES_AUTO_POPULATE_CONTENT = True

DBTEMPLATES_ADD_DEFAULT_SITE = True

MIDDLEWARE_CLASSES = default.middlewares

ROOT_URLCONF = 'leonardo.urls'

location = lambda x: os.path.join(
    os.path.dirname(os.path.realpath(__file__)), x)

TEMPLATE_DIRS = (
    location('templates'),
)

MARKITUP_FILTER = ('markitup.renderers.render_rest', {'safe_mode': True})

INSTALLED_APPS = default.apps

#ADMIN_TOOLS_MENU = 'hrcms.conf.menu.AdminDashboard'
#ADMIN_TOOLS_INDEX_DASHBOARD = 'hrcms.conf.menu.AdminDashboard'

# For easy_thumbnails to support retina displays (recent MacBooks, iOS)

THUMBNAIL_HIGH_RESOLUTION = True

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

# File download permissions are an experimental
# feature. The api may change at any time.

FILER_ENABLE_PERMISSIONS = True

FEINCMS_USE_PAGE_ADMIN = False

FEINCMS_DEFAULT_PAGE_MODEL = 'web.Page'

##########################

STATICFILES_FINDERS =(
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    'compressor.finders.CompressorFinder',
)

LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_URL = "/"

LOGOUT_ON_GET = True

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING',
        'handlers': ['file'],
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
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
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/srv/hrcms/logs/hrcms_server.log',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

# migrations support
MIGRATION_MODULES = {
    'application': 'leonardo.migrations.application',
    'filer': 'filer.migrations_django',
}

CRISPY_TEMPLATE_PACK = 'bootstrap'

SECRET_KEY = None

APPS = []

try:
    # local settings
    from local_settings import *
except ImportError:
    pass

try:
    # full settings
    from leonardo_site.local.settings import *
except ImportError:
    pass

if not SECRET_KEY:
    LOCAL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'local')

    from horizon.utils import secret_key

    SECRET_KEY = secret_key.generate_or_read_from_file(os.path.join(LOCAL_PATH,
                                                                    '.secret_key_store'))
from oscar.defaults import *

REVERSION_MIDDLEWARE=[
    'reversion.middleware.RevisionMiddleware']


OAUTH_CTP = [
    "allauth.socialaccount.context_processors.socialaccount"
]

# first load some defaults

try:
    from leonardo.conf.horizon import *
    from leonardo.conf.static import *
except Exception, e:
    raise e


# import defaults
"""
#from leonardo.module.web import default as web_default
from leonardo.module.nav import default as nav_default
from leonardo.module.lang import default as lang_default
from leonardo.module.forms import default as forms_default
"""

APPLICATION_CHOICES = [] # init

if 'media' in APPS:
    FILER_IMAGE_MODEL = 'leonardo.module.media.models.Image'

from leonardo.module.web.settings import *
from leonardo.module.web.models import Page
from leonardo.module.web.widget import ApplicationWidget

from leonardo.module.eshop import default
try:
    # override settings
    try:
        from leonardo_site.conf.feincms import *
    except ImportError:
        pass

    from django.utils.importlib import import_module  # noqa

    from django.utils.module_loading import module_has_submodule  # noqa

    # Try importing a modules from the module package
    package_string = '.'.join(['leonardo', 'module'])

    # can be merged into one for cycle
    # collect application settings
    for app in APPS:
        try:
            # check if is not full app
            _app = import_module(app)
        except ImportError:
            _app = False
        if module_has_submodule(import_module(package_string), app) or _app:
            if _app:
                mod = _app
            else:
                mod = import_module('.{0}'.format(app), package_string)

            if hasattr(mod, 'default'):

                APPLICATION_CHOICES = merge(APPLICATION_CHOICES, getattr(
                        mod.default, 'plugins', []))

                INSTALLED_APPS = merge(
                    INSTALLED_APPS, getattr(mod.default, 'apps', []))

                TEMPLATE_CONTEXT_PROCESSORS = merge(
                    TEMPLATE_CONTEXT_PROCESSORS, getattr(
                        mod.default, 'ctp', []))
                MIDDLEWARE_CLASSES = merge(
                                            MIDDLEWARE_CLASSES, getattr(
                                            mod.default, 'middlewares', []))
                AUTHENTICATION_BACKENDS = merge(
                    AUTHENTICATION_BACKENDS, getattr(
                        mod.default, 'auth_backends', []))
    # register external apps
    Page.create_content_type(
        ApplicationWidget, APPLICATIONS=APPLICATION_CHOICES)

    # register widgets
    for app in APPS:
        if module_has_submodule(import_module(package_string), app):
            mod = import_module('.{0}'.format(app), package_string)

            if hasattr(mod, 'default'):

                for ct in getattr(mod.default, 'widgets', []):

                    Page.create_content_type(
                        ct, optgroup=getattr(
                            mod.default, 'optgroup', app.capitalize()))

    Page.register_extensions(*PAGE_EXTENSIONS)
    Page.register_default_processors(
        frontend_editing=True)
except Exception, e:
    raise e

if 'fulltext' or 'eshop' in APPS:

    # search
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
            'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
        },
    }

    INSTALLED_APPS = merge(['whoosh'], INSTALLED_APPS)

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
