
from __future__ import absolute_import

import os
from os.path import abspath, dirname, join, normpath

from oscar import get_core_apps, OSCAR_MAIN_TEMPLATE_DIR

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
    ('newt', 'mail@newt.cz'),
    ('majklk', 'mail@majklk.cz'),
)

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

MEDIA_ROOT = '/srv/hrcms/media/'
MEDIA_URL = '/media/'
STATIC_ROOT = '/srv/hrcms/static/'
STATIC_URL = '/static/'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    "allauth.socialaccount.context_processors.socialaccount",
    # horizon
    'horizon.context_processors.horizon',
    # feinCMS
    'feincms.context_processors.add_page_if_missing',
    # oscar
    'oscar.apps.search.context_processors.search_form',
    'oscar.apps.promotions.context_processors.promotions',
    'oscar.apps.checkout.context_processors.checkout',
    'oscar.apps.customer.notifications.context_processors.notifications',
    'oscar.core.context_processors.metadata',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # horizon
    'hrcms.middleware.HorizonMiddleware',

    # oscar
    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'hrcms.urls'

location = lambda x: os.path.join(
    os.path.dirname(os.path.realpath(__file__)), x)

TEMPLATE_DIRS = (
    location('templates'),
    OSCAR_MAIN_TEMPLATE_DIR,
)

MARKITUP_FILTER = ('markitup.renderers.render_rest', {'safe_mode': True})

INSTALLED_APPS = [
    'django',

    # admin tools
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'flat',  # theme

    'django_extensions',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',

    'rest_framework',
    'oscarapi',

    'hrcms.module.boardie',

    #'hrcms.module.graph',
    #'hrcms.module.time',
    #'hrcms.module.time_series',

    #'boardie',

    'django_select2',

    'livesettings',


    'form_designer',
    'django_remote_forms',

    'horizon',
    'compressor',

    # filer
    'filer',
    'easy_thumbnails',

    # CMS
    'markitup',
    'feincms',
    'mptt',
    'feincms.module.page',
    'feincms.module.blog',
    'feincms.module.medialibrary',
    'feincms.content.application',
    'feincms.content.comments',

    'hrcms',
    'hrcms.module',
    'hrcms.module.eshop',
    'hrcms.module.eshop.api',
    'hrcms.module.nav',
    'hrcms.module.lang',
    'hrcms.module.web',
    'hrcms.module.forms',

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

    'hrcms_site',

] + get_core_apps() # oscar apps

#ADMIN_TOOLS_MENU = 'hrcms.conf.menu.AdminDashboard'
#ADMIN_TOOLS_INDEX_DASHBOARD = 'hrcms.conf.menu.AdminDashboard'

# OSCAR 

OSCAR_INITIAL_ORDER_STATUS = 'Pending'
OSCAR_INITIAL_LINE_STATUS = 'Pending'
OSCAR_ORDER_STATUS_PIPELINE = {
    'Pending': ('Being processed', 'Cancelled',),
    'Being processed': ('Processed', 'Cancelled',),
    'Cancelled': (),
}

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
    "allauth.account.auth_backends.AuthenticationBackend",
    'oscar.apps.customer.auth_backends.EmailBackend',
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

DEFAULT_CHARSET = 'utf-8'

# search
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

INSTALLED_APPS += ['whoosh']

# migrations support
MIGRATION_MODULES = {
    'page': 'hrcms.migrations.page',
    #'boardie': 'boardie.migrations',
    'application': 'hrcms.migrations.application',
    'filer': 'filer.migrations_django',
}

SECRET_KEY = None

# helper
# noqa 
from local_settings import *

if not SECRET_KEY:
    LOCAL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'local')

    from horizon.utils import secret_key

    SECRET_KEY = secret_key.generate_or_read_from_file(os.path.join(LOCAL_PATH,
                                                                    '.secret_key_store'))

try:
    from hrcms.conf.feincms import *
    from hrcms.conf.horizon import *
    from oscar.defaults import *
    from hrcms.conf.static import *
except Exception, e:
    raise e

from local_settings import *

try:
    import hrcms_site
    from hrcms_site.conf.settings import *
except Exception, e:
    raise e
