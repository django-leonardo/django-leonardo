
from __future__ import absolute_import

import os
from os.path import abspath, dirname, join, normpath

from django import VERSION
import six
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

SITE_NAME = 'Leonardo'

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


if VERSION[:2] >= (1, 8):

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
LOGIN_REDIRECT_URL = '/'
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

PAGE_EXTENSIONS = []

# use default leonardo auth urls
LEONARDO_AUTH = True

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

ADD_JS_FILES = []

ADD_CSS_FILES = []

ADD_JS_SPEC_FILES = []

try:

    # override settings
    try:
        from leonardo_site.conf.feincms import *
    except ImportError:
        pass

    from django.utils.importlib import import_module  # noqa

    from django.utils.module_loading import module_has_submodule  # noqa

    widgets = {}

    from leonardo import get_conf_from_module, merge

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

        mod_cfg = get_conf_from_module(mod)

        APPLICATION_CHOICES = merge(APPLICATION_CHOICES, mod_cfg.plugins)

        INSTALLED_APPS = merge(INSTALLED_APPS, mod_cfg.apps)

        MIDDLEWARE_CLASSES = merge(MIDDLEWARE_CLASSES, mod_cfg.middlewares)
        AUTHENTICATION_BACKENDS = merge(
            AUTHENTICATION_BACKENDS, mod_cfg.auth_backends)

        PAGE_EXTENSIONS = merge(PAGE_EXTENSIONS, mod_cfg.page_extensions)

        ADD_JS_FILES = merge(ADD_JS_FILES, mod_cfg.js_files)

        ADD_JS_SPEC_FILES = merge(ADD_JS_SPEC_FILES, mod_cfg.js_spec_files)

        ADD_CSS_FILES = merge(ADD_CSS_FILES, mod_cfg.css_files)

        if VERSION[:2] >= (1, 8):
            TEMPLATES[0]['DIRS'] = merge(TEMPLATES[0]['DIRS'], mod_cfg.dirs)
            cp = TEMPLATES[0]['OPTIONS']['context_processors']
            TEMPLATES[0]['OPTIONS']['context_processors'] = merge(
                cp, mod_cfg.context_processors)

        else:

            TEMPLATE_CONTEXT_PROCESSORS = merge(
                TEMPLATE_CONTEXT_PROCESSORS, mod_cfg.context_processors)
            TEMPLATE_DIRS = merge(TEMPLATE_DIRS, mod_cfg.dirs)

        # collect grouped widgets
        opt_group = mod_cfg.optgroup or app.capitalize()
        widgets[opt_group] = merge(
            getattr(widgets, opt_group, []), mod_cfg.widgets)

    setattr(leonardo, 'js_files', ADD_JS_FILES)
    setattr(leonardo, 'css_files', ADD_CSS_FILES)
    setattr(leonardo, 'js_spec_files', ADD_JS_SPEC_FILES)
    setattr(leonardo, 'widgets', widgets)


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

setattr(leonardo, 'apps', APPS)
setattr(leonardo, 'page_extensions', PAGE_EXTENSIONS)
setattr(leonardo, 'plugins', APPLICATION_CHOICES)

# ensure if bootstra_admin is on top of INSTALLED_APPS
if 'bootstrap_admin' in INSTALLED_APPS:
    BOOTSTRAP_ADMIN_SIDEBAR_MENU = True
    # INSTALLED_APPS.remove('bootstrap_admin')
    #INSTALLED_APPS = ['bootstrap_admin'] + INSTALLED_APPS

# Add HORIZON_CONFIG to the context information for offline compression
COMPRESS_OFFLINE_CONTEXT = {
    'STATIC_URL': STATIC_URL,
    'HORIZON_CONFIG': HORIZON_CONFIG,
}

try:
    import debug_toolbar
    INSTALLED_APPS += ['debug_toolbar']
    INTERNAL_IPS = ['10.10.10.1', '127.0.0.1']
except ImportError:
    pass

# use js files instead of horizon
HORIZON_CONFIG['js_files'] = leonardo.js_files
HORIZON_CONFIG['js_spec_files'] = leonardo.js_spec_files
HORIZON_CONFIG['css_files'] = leonardo.css_files
# path horizon config
from horizon import conf
conf.HORIZON_CONFIG = HORIZON_CONFIG
