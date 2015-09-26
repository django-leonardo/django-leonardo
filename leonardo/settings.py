
from __future__ import absolute_import

import os
import six
import logging
import warnings

from django import VERSION
from leonardo.base import leonardo, default
from leonardo.utils.settings import (get_conf_from_module, merge,
                                     get_leonardo_modules, get_loaded_modules)


_file_path = os.path.abspath(os.path.dirname(__file__)).split('/')

BASE_DIR = '/'.join(_file_path[0:-2])

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
    ('en', 'EN'),
    ('cs', 'CS'),
)

USE_I18N = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

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

LEONARDO_BOOTSTRAP_URL = 'http://github.com/django-leonardo/django-leonardo/raw/develop/contrib/bootstrap/demo.yaml'

MARKITUP_FILTER = ('markitup.renderers.render_rest', {'safe_mode': True})

INSTALLED_APPS = default.apps

# For easy_thumbnails to support retina displays (recent MacBooks, iOS)

FEINCMS_USE_PAGE_ADMIN = False

LEONARDO_USE_PAGE_ADMIN = True

FEINCMS_DEFAULT_PAGE_MODEL = 'web.Page'

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {}

# enable auto loading packages
LEONARDO_MODULE_AUTO_INCLUDE = True

# enable system module
LEONARDO_SYSTEM_MODULE = True

##########################


STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    'compressor.finders.CompressorFinder',
)

LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = "/auth/logout"

LOGOUT_ON_GET = True

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'DEBUG',
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
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'leonardo_app.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'leonardo': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

CRISPY_TEMPLATE_PACK = 'bootstrap3'

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
    warnings.warn(
        'local_settings was not found in $PYTHONPATH !',
        ImportWarning)

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
except Exception as e:
    pass

FEINCMS_TIDY_HTML = False

APPLICATION_CHOICES = []

ADD_JS_FILES = []

ADD_CSS_FILES = []

ADD_SCSS_FILES = []

ADD_JS_SPEC_FILES = []

ADD_ANGULAR_MODULES = []

ADD_PAGE_ACTIONS = []

ADD_WIDGET_ACTIONS = []

MIGRATION_MODULES = {}

ADD_MIGRATION_MODULES = {}

CONSTANCE_CONFIG_GROUPS = {}

ABSOLUTE_URL_OVERRIDES = {}

MODULE_URLS = {}

if LEONARDO_SYSTEM_MODULE:
    APPS = merge(APPS, ['leonardo_system'])
    HORIZON_CONFIG['system_module'] = True
else:
    HORIZON_CONFIG['system_module'] = False

# override settings
try:
    from leonardo_site.conf.feincms import *
except ImportError:
    pass

from django.utils.importlib import import_module  # noqa

from django.utils.module_loading import module_has_submodule  # noqa

WIDGETS = {}

# critical time to import modules
_APPS = leonardo.get_app_modules(APPS)

if LEONARDO_MODULE_AUTO_INCLUDE:
    # fined and merge with defined app modules
    _APPS = merge(get_leonardo_modules(), _APPS)

# iterate over sorted modules
for mod, mod_cfg in get_loaded_modules(_APPS):

    try:

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
                warnings.warn(
                    'Exception "{}" raised during loading '
                    'settings from {}'.format(str(e), mod))

        APPLICATION_CHOICES = merge(APPLICATION_CHOICES, mod_cfg.plugins)

        INSTALLED_APPS = merge(INSTALLED_APPS, mod_cfg.apps)

        MIDDLEWARE_CLASSES = merge(MIDDLEWARE_CLASSES, mod_cfg.middlewares)
        AUTHENTICATION_BACKENDS = merge(
            AUTHENTICATION_BACKENDS, mod_cfg.auth_backends)

        PAGE_EXTENSIONS = merge(PAGE_EXTENSIONS, mod_cfg.page_extensions)

        ADD_JS_FILES = merge(ADD_JS_FILES, mod_cfg.js_files)

        ADD_PAGE_ACTIONS = merge(ADD_PAGE_ACTIONS, mod_cfg.page_actions)
        ADD_WIDGET_ACTIONS = merge(ADD_WIDGET_ACTIONS, mod_cfg.widget_actions)

        if mod_cfg.urls_conf:
            MODULE_URLS[mod_cfg.urls_conf] = {'is_public': mod_cfg.public}

        # TODO move to utils.settings
        # support for one level nested in config dictionary
        for config_key, config_value in six.iteritems(mod_cfg.config):
            if isinstance(config_value, dict):
                CONSTANCE_CONFIG_GROUPS.update({config_key: config_value})
                for c_key, c_value in six.iteritems(config_value):
                    mod_cfg.config[c_key] = c_value
                # remove from main dict
                mod_cfg.config.pop(config_key)
            else:
                if isinstance(mod_cfg.optgroup, six.string_types):
                    CONSTANCE_CONFIG_GROUPS.update({
                        mod_cfg.optgroup: mod_cfg.config})
                else:
                    CONSTANCE_CONFIG_GROUPS.update({
                        'ungrouped': mod_cfg.config})

        # import and update absolute overrides
        for model, method in six.iteritems(mod_cfg.absolute_url_overrides):
            try:
                _mod = import_module(".".join(method.split('.')[:-1]))
                ABSOLUTE_URL_OVERRIDES[model] = getattr(_mod, method.split('.')[-1])
            except Exception as e:
                raise e

        for nav_extension in mod_cfg.navigation_extensions:
            try:
                import_module(nav_extension)
            except ImportError:
                pass

        CONSTANCE_CONFIG.update(mod_cfg.config)
        ADD_MIGRATION_MODULES.update(mod_cfg.migration_modules)

        ADD_JS_SPEC_FILES = merge(ADD_JS_SPEC_FILES, mod_cfg.js_spec_files)

        ADD_CSS_FILES = merge(ADD_CSS_FILES, mod_cfg.css_files)
        ADD_SCSS_FILES = merge(ADD_SCSS_FILES, mod_cfg.scss_files)

        ADD_ANGULAR_MODULES = merge(
            ADD_ANGULAR_MODULES, mod_cfg.angular_modules)

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
        if isinstance(mod_cfg.optgroup, six.string_types):
            WIDGETS[mod_cfg.optgroup] = merge(
                getattr(WIDGETS, mod_cfg.optgroup, []), mod_cfg.widgets)
        else:
            if DEBUG:
                warnings.warn('You have ungrouped widgets'
                              ', please specify your ``optgroup``'
                              'which categorize your widgets')
            WIDGETS['ungrouped'] = merge(
                getattr(WIDGETS, 'ungrouped', []), mod_cfg.widgets)

    except Exception as e:
        warnings.warn(
            'Exception "{}" raised during loading '
            'module {}'.format(str(e), mod))

setattr(leonardo, 'js_files', ADD_JS_FILES)
setattr(leonardo, 'css_files', ADD_CSS_FILES)
setattr(leonardo, 'scss_files', ADD_SCSS_FILES)
setattr(leonardo, 'js_spec_files', ADD_JS_SPEC_FILES)
setattr(leonardo, 'angular_modules', ADD_ANGULAR_MODULES)
setattr(leonardo, 'page_actions', ADD_PAGE_ACTIONS)
setattr(leonardo, 'widget_actions', ADD_WIDGET_ACTIONS)
setattr(leonardo, 'widgets', WIDGETS)

from leonardo.module.web.models import Page
from leonardo.module.web.widget import ApplicationWidget

# register external apps
Page.create_content_type(
    ApplicationWidget, APPLICATIONS=APPLICATION_CHOICES)

# register widgets
for optgroup, _widgets in six.iteritems(WIDGETS):
    for widget in _widgets:
        Page.create_content_type(widget, optgroup=optgroup)

Page.register_extensions(*PAGE_EXTENSIONS)
Page.register_default_processors(LEONARDO_FRONTEND_EDITING)

# enable reversion for every req
if 'reversion' in INSTALLED_APPS:
    MIDDLEWARE_CLASSES = merge(REVERSION_MIDDLEWARE, MIDDLEWARE_CLASSES)

# FINALLY OVERRIDE ALL

try:
    # local settings
    from local_settings import *
except ImportError:
    warnings.warn(
        'Missing local_settings !')

try:
    # full settings
    from leonardo_site.local.settings import *
except ImportError:
    pass

# and again merge core with others
APPS = merge(APPS, default.core)

setattr(leonardo, 'apps', APPS)
setattr(leonardo, 'page_extensions', PAGE_EXTENSIONS)
setattr(leonardo, 'plugins', APPLICATION_CHOICES)

MIGRATION_MODULES.update(ADD_MIGRATION_MODULES)

# Add HORIZON_CONFIG to the context information for offline compression
COMPRESS_OFFLINE_CONTEXT = {
    'STATIC_URL': STATIC_URL,
    'HORIZON_CONFIG': HORIZON_CONFIG,
}

if DEBUG:
    # debug
    try:
        import debug_toolbar
        INSTALLED_APPS = merge(INSTALLED_APPS, ['debug_toolbar'])
        INTERNAL_IPS = ['10.10.10.1', '127.0.0.1']
        DEBUG_TOOLBAR_PANELS = [
            'debug_toolbar.panels.versions.VersionsPanel',
            'debug_toolbar.panels.timer.TimerPanel',
            'debug_toolbar.panels.settings.SettingsPanel',
            'debug_toolbar.panels.headers.HeadersPanel',
            'debug_toolbar.panels.request.RequestPanel',
            'debug_toolbar.panels.sql.SQLPanel',
            'debug_toolbar.panels.staticfiles.StaticFilesPanel',
            'debug_toolbar.panels.templates.TemplatesPanel',
            'debug_toolbar.panels.cache.CachePanel',
            'debug_toolbar.panels.signals.SignalsPanel',
            'debug_toolbar.panels.logging.LoggingPanel',
            'debug_toolbar.panels.redirects.RedirectsPanel',
            'debug_toolbar.panels.profiling.ProfilingPanel'
        ]

    except ImportError:
        if DEBUG:
            warnings.warn('DEBUG is set to True but, DEBUG tools '
                          'is not installed please run '
                          '"pip install django-leonardo[debug]"')

# async messages
try:
    import async_messages
    INSTALLED_APPS = merge(INSTALLED_APPS, ['async_messages'])
    MIDDLEWARE_CLASSES = merge(MIDDLEWARE_CLASSES,
                               ['async_messages.middleware.AsyncMiddleware'])
except ImportError:
    pass
    """
    LOG.debug('ASYNC MESSAGES is not installed'
              ' install for new messaging features '
              '"pip install django-async-messages"')
    """


# use js files instead of horizon
HORIZON_CONFIG['js_files'] = leonardo.js_files
HORIZON_CONFIG['js_spec_files'] = leonardo.js_spec_files
HORIZON_CONFIG['css_files'] = leonardo.css_files
HORIZON_CONFIG['scss_files'] = leonardo.scss_files
HORIZON_CONFIG['angular_modules'] = leonardo.angular_modules
HORIZON_CONFIG['page_actions'] = leonardo.page_actions
HORIZON_CONFIG['widget_actions'] = leonardo.widget_actions
# path horizon config
from horizon import conf
conf.HORIZON_CONFIG = HORIZON_CONFIG

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
