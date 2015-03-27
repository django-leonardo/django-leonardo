
from os.path import join, dirname, abspath, normpath

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'PORT': '5432',
        'HOST': '127.0.0.1',
        'NAME': 'hrcms',
        'PASSWORD': 'pwd',
        'USER': 'hrcms'
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 120,
        'KEY_PREFIX': 'CACHE_ROBOTICE_SITE'
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

SECRET_KEY = '6549874asdasdASD56451xyasdASDDSAsd'

ALLOWED_HOSTS = ['*']

SOUTH_TESTS_MIGRATE = False

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
    'horizon.context_processors.horizon',
    'feincms.context_processors.add_page_if_missing', # good point
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
    'hrcms.middleware.HorizonMiddleware',
)

ROOT_URLCONF = 'hrcms.urls'

TEMPLATE_DIRS = (
)

MARKITUP_FILTER = ('markitup.renderers.render_rest', {'safe_mode': True})

INSTALLED_APPS = (
    'django',
    'django_extensions',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',

    'hrcms',
    'hrcms.module',
    #'hrcms.portal',
    
    'boardie',

    'horizon',
    'compressor',
    #'django_select2',

    # filer
    'filer',
    'easy_thumbnails',

    'markitup',
    'feincms',
    'mptt',
    'feincms.module.page',
    'feincms.module.blog',
    'feincms.module.medialibrary',
    'feincms.content.application',
    'feincms.content.comments',

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
)

# For easy_thumbnails to support retina displays (recent MacBooks, iOS)

#THUMBNAIL_HIGH_RESOLUTION = True

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
    'page': 'hrcms.migrations.page',
    'boardie': 'boardie.migrations',
    'application': 'hrcms.migrations.application',
    'filer': 'filer.migrations_django',
}


# include FEIN_CMS and HORIZON conf
try:
    from hrcms.conf.feincms import *
    from hrcms.conf.horizon import *
    #from boardie.conf.django import *
except Exception, e:
    raise e

# override all
try:
    from local_settings import *
except Exception, e:
    raise e