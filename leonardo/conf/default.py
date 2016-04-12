
from leonardo.base import default

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

ADMINS = (
    ('admin', 'mail@leonardo.cz'),
)

# month
LEONARDO_CACHE_TIMEOUT = 60 * 60 * 24 * 31

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

DBTEMPLATES_MEDIA_PREFIX = '/static-/'

DBTEMPLATES_AUTO_POPULATE_CONTENT = True

DBTEMPLATES_ADD_DEFAULT_SITE = True

FILER_ENABLE_PERMISSIONS = True  # noqa

MIDDLEWARE_CLASSES = default.middlewares

ROOT_URLCONF = 'leonardo.urls'

LEONARDO_BOOTSTRAP_URL = 'http://github.com/django-leonardo/django-leonardo/raw/master/contrib/bootstrap/demo.yaml'

MARKITUP_FILTER = ('markitup.renderers.render_rest', {'safe_mode': True})

INSTALLED_APPS = default.apps

# For easy_thumbnails to support retina displays (recent MacBooks, iOS)

FEINCMS_USE_PAGE_ADMIN = False

LEONARDO_USE_PAGE_ADMIN = True

FEINCMS_DEFAULT_PAGE_MODEL = 'web.Page'

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {}

CONSTANCE_ADDITIONAL_FIELDS = {}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

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


LOGIN_URL = '/auth/login'

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
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'leonardo': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

CRISPY_TEMPLATE_PACK = 'bootstrap3'

SECRET_KEY = None

APPS = []

PAGE_EXTENSIONS = []

MIGRATION_MODULES = {}

# use default leonardo auth urls
LEONARDO_AUTH = True

FEINCMS_TIDY_HTML = False

APPLICATION_CHOICES = []

ADD_JS_FILES = []

ADD_CSS_FILES = []

ADD_SCSS_FILES = []

ADD_JS_SPEC_FILES = []

ADD_ANGULAR_MODULES = []

ADD_PAGE_ACTIONS = []

ADD_WIDGET_ACTIONS = []

ADD_MIGRATION_MODULES = {}

ADD_JS_COMPRESS_FILES = []

CONSTANCE_CONFIG_GROUPS = {}

ABSOLUTE_URL_OVERRIDES = {}

SELECT2_CACHE_PREFIX = 'SELECT2'

MODULE_URLS = {}

WIDGETS = {}
