
from __future__ import absolute_import

import os
from os.path import abspath, dirname, join, normpath

from oscar import get_core_apps as get_eshop_apps, OSCAR_MAIN_TEMPLATE_DIR

from hrcms import default, merge

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
    ('admin', 'mail@hrcms.cz'),
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
MEDIA_ROOT = '/srv/hrcms/media/'
STATIC_ROOT = '/srv/hrcms/static/'

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

TEMPLATE_CONTEXT_PROCESSORS = default.ctp

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


MIDDLEWARE_CLASSES = default.middlewares

ROOT_URLCONF = 'hrcms.urls'

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
    'application': 'hrcms.migrations.application',
    'filer': 'filer.migrations_django',
}

SECRET_KEY = None

APPS = []

try:
    # local settings
    from local_settings import *
except ImportError:
    pass

try:
    # full settings
    from hrcms_site.local.settings import *
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

ESHOP_MIDDLEWARE=[
    'oscar.apps.basket.middleware.BasketMiddleware']

ESHOP_CONTEXT_PROCESSORS=[
    'oscar.apps.search.context_processors.search_form',
    'oscar.apps.promotions.context_processors.promotions',
    'oscar.apps.checkout.context_processors.checkout',
    'oscar.apps.customer.notifications.context_processors.notifications',
    'oscar.core.context_processors.metadata',
]

ESHOP_APPS = [
    'hrcms.module.eshop',
    'hrcms.module.eshop.api',
    'oscarapi'] + get_eshop_apps()

ESHOP_AUTH_BACKENDS = [
    'oscar.apps.customer.auth_backends.EmailBackend',
]

BLOG_APPS = ['elephantblog', 'hrcms.module.blog']

OAUTH_BACKENDS = [
    "allauth.account.auth_backends.AuthenticationBackend",
]

OAUTH_CTP = [
    "allauth.socialaccount.context_processors.socialaccount"
]

OAUTH_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.amazon',
    'allauth.socialaccount.providers.angellist',
    'allauth.socialaccount.providers.bitbucket',
    'allauth.socialaccount.providers.bitly',
    'allauth.socialaccount.providers.coinbase',
    'allauth.socialaccount.providers.dropbox',
    #'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.flickr',
    'allauth.socialaccount.providers.feedly',
    'allauth.socialaccount.providers.fxa',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.hubic',
    'allauth.socialaccount.providers.instagram',
    'allauth.socialaccount.providers.linkedin',
    'allauth.socialaccount.providers.linkedin_oauth2',
    'allauth.socialaccount.providers.odnoklassniki',
    'allauth.socialaccount.providers.openid',
    'allauth.socialaccount.providers.persona',
    'allauth.socialaccount.providers.soundcloud',
    'allauth.socialaccount.providers.stackexchange',
    'allauth.socialaccount.providers.tumblr',
    'allauth.socialaccount.providers.twitch',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.vimeo',
    'allauth.socialaccount.providers.vk',
    'allauth.socialaccount.providers.weibo',
    'allauth.socialaccount.providers.xing',
]

# first load some defaults

try:
    from hrcms.conf.horizon import *
    from hrcms.conf.static import *
except Exception, e:
    raise e

# register common stuff

"""aggregate for some apps

    - cms
    - blog
    - eshop
    - oauth
    - reversion
    - fulltext

"""

if 'cms' in APPS:

    # import defaults
    from hrcms.module.web import default as web_default
    from hrcms.module.web.settings import *
    from hrcms.module.web.models import Page
    from feincms.content.application.models import ApplicationContent

    try:
        # override settings
        from project.conf.feincms import *

        # register stuff
        Page.create_content_type(
            ApplicationContent, APPLICATIONS=APPLICATION_CHOICES)
        for ct in CONTENT_TYPES:
            Page.create_content_type(ct)
        Page.register_extensions(*PAGE_EXTENSIONS)
        Page.register_default_processors(
            frontend_editing=FEINCMS_FRONTEND_EDITING)
    except ImportError:
        pass
    except Exception, e:
        raise e

    INSTALLED_APPS = merge(INSTALLED_APPS, web_default.apps)
    TEMPLATE_CONTEXT_PROCESSORS = merge(
        TEMPLATE_CONTEXT_PROCESSORS, web_default.ctp)
    MIDDLEWARE_CLASSES = merge(MIDDLEWARE_CLASSES, web_default.middlewares)

if 'blog' in APPS:
    INSTALLED_APPS = merge(INSTALLED_APPS, BLOG_APPS)

if 'oauth' in APPS:
    INSTALLED_APPS = merge(INSTALLED_APPS, OAUTH_APPS)
    TEMPLATE_CONTEXT_PROCESSORS = merge(
        OAUTH_CTP, TEMPLATE_CONTEXT_PROCESSORS)
    AUTHENTICATION_BACKENDS = merge(AUTHENTICATION_BACKENDS, OAUTH_BACKENDS)

# configure eshop
if 'eshop' in APPS or 'oscar' in INSTALLED_APPS:

    INSTALLED_APPS = merge(INSTALLED_APPS, ESHOP_APPS)
    MIDDLEWARE_CLASSES = merge(MIDDLEWARE_CLASSES, ESHOP_MIDDLEWARE)
    TEMPLATE_CONTEXT_PROCESSORS = merge(
        ESHOP_CONTEXT_PROCESSORS, TEMPLATE_CONTEXT_PROCESSORS)
    AUTHENTICATION_BACKENDS = merge(
        AUTHENTICATION_BACKENDS, ESHOP_AUTH_BACKENDS)

    # OSCAR SPECIFIC CONF

    OSCAR_INITIAL_ORDER_STATUS = 'Pending'
    OSCAR_INITIAL_LINE_STATUS = 'Pending'
    OSCAR_ORDER_STATUS_PIPELINE = {
        'Pending': ('Being processed', 'Cancelled',),
        'Being processed': ('Processed', 'Cancelled',),
        'Cancelled': (),
    }
    TEMPLATE_DIRS = merge(TEMPLATE_DIRS, OSCAR_MAIN_TEMPLATE_DIR)

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
