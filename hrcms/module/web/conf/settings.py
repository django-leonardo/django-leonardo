from os.path import join, dirname, abspath


try:
    from project.conf.settings import SITE_NAME, SITE_DOMAIN, ENV_ROOT
except ImportError:
    from conf.settings import SITE_NAME, SITE_DOMAIN, ENV_ROOT

try:
    from project.config import DEFAULT_DATABASE, DEFAULT_CACHE, DEFAULT_EMAIL
    CONFIG_LOADED = True
except ImportError:
    try:
        from config import DEFAULT_DATABASE, DEFAULT_CACHE, DEFAULT_EMAIL
        CONFIG_LOADED = True
    except ImportError:
        DEFAULT_DATABASE = {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': '127.0.0.1',
            'PORT': '5432',
            'NAME': 'django12_%s_prod' % SITE_NAME,
            'PASSWORD': 'pass_%s' % SITE_NAME,
            'USER': 'django12_%s_prod' % SITE_NAME
        }
        DEFAULT_CACHE = {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
            'TIMEOUT': 120,
            'KEY_PREFIX': "CACHE_%s" % SITE_NAME.upper()
        }
        DEFAULT_EMAIL = {
            'HOST': 'mail.highline.cz',
            'PORT': '25',
            'USER': 'robot@highline.cz',
            'PASSWORD': 'Bender240',
        }
        CONFIG_LOADED = False

#DEFAULT_EMAIL = {
#    'HOST': 'mail.highline.cz',
#    'USER': 'robot@highline.cz',
#    'PASSWORD': 'Bender240',
#}

CACHES = {
    'default': DEFAULT_CACHE
}

DATABASES = {
    'default': DEFAULT_DATABASE
}

DEBUG = False
TEMPLATE_DEBUG = DEBUG

EMAIL_HOST = DEFAULT_EMAIL['HOST']

if DEFAULT_EMAIL.has_key('PORT'):
    EMAIL_PORT = DEFAULT_EMAIL['PORT']

if DEFAULT_EMAIL.has_key('SECURITY'):

    if DEFAULT_EMAIL['SECURITY'] == 'SSL':
        EMAIL_USE_SSL = True

    if DEFAULT_EMAIL['SECURITY'] == 'TLS':
        EMAIL_USE_TLS = True

EMAIL_HOST_USER = DEFAULT_EMAIL['USER']
EMAIL_HOST_PASSWORD = DEFAULT_EMAIL['PASSWORD']

DEFAULT_FROM_EMAIL = 'no_reply@%s' % SITE_DOMAIN
SERVER_EMAIL = 'no_reply@%s' % SITE_DOMAIN

EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME.upper()

try:
    try:
        from project.config import RAVEN_CONFIG
    except ImportError:
        from config import RAVEN_CONFIG
    if RAVEN_CONFIG.get("dsn", None):
        RAVEN = True
    else:
        RAVEN = False
except ImportError:
    RAVEN = False

try:
    from project.config import DEFAULT_GOOGLE_ANALYTICS
except ImportError:
    try:
        from config import DEFAULT_GOOGLE_ANALYTICS
    except ImportError:
        DEFAULT_GOOGLE_ANALYTICS = None

if DEFAULT_GOOGLE_ANALYTICS != None:
    GOOGLE_ANALYTICS_USER_EMAIL = DEFAULT_GOOGLE_ANALYTICS["USER_EMAIL"]
    GOOGLE_ANALYTICS_USER_PASS = DEFAULT_GOOGLE_ANALYTICS["USER_PASSWORD"]
    GOOGLE_ANALYTICS_PROPERTY_ID = DEFAULT_GOOGLE_ANALYTICS["PROPERTY_ID"]

MEDIA_ROOT = join(ENV_ROOT, 'sites', SITE_NAME, 'media')
MEDIA_URL = '/media/'

WEBCMS_MEDIA_ROOT = join(MEDIA_ROOT, 'files')
WEBCMS_MEDIA_URL = '/media/files/'

ADMINS = (
    ('Admin', 'webmaster@htfs.info'),
)

USE_I18N = True

ADMIN_MEDIA_PREFIX = '/static/lib/webcms/'
FEINCMS_ADMIN_MEDIA = '/static/lib/webcms/'


FEINCMS_TREE_EDITOR_INCLUDE_ANCESTORS = True
#FEINCMS_TIDY_HTML = True

#TEMPLATE_LOADERS = (
#    'django.template.loaders.filesystem.load_template_source',
#    'webcms.loader.load_template_source',
#    'django.template.loaders.app_directories.load_template_source',
#    'django.template.loaders.eggs.load_template_source',
#)

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)


MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.doc.XViewMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "pagination.middleware.PaginationMiddleware",
    "browser_info.Middleware",
    "webcms.middleware.WebCmsMiddleware",
#    "django_statsd.middleware.StatsdMiddlewareTimer",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
)

#if RAVEN:
#    EXTRA_MIDDLEWARE_CLASSES = (
#      'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
#    )

TEMPLATE_DIRS = (
    join(ENV_ROOT, 'sites', SITE_NAME, 'project', 'conf', 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'project.conf.urls'

DAJAXICE_MEDIA_PREFIX = "dajaxice"
DAJAXICE_JSON2_JS_IMPORT = False

ASSETS_CACHE = "_cache/assets"
ASSETS_DEBUG = False

# completely unrelated to other assets
ASSETS_LOCAL = False

ADMIN_TOOLS_MENU = 'project.conf.menu.AdminDashboard'

HAYSTACK_SITECONF = 'webcms.search'
HAYSTACK_SEARCH_ENGINE = 'dummy'
#HAYSTACK_SOLR_URL = 'http://127.0.0.1:8080/solr'

THUMBNAIL_PREFIX = '_cache/thumbnails/'
THUMBNAIL_UPSCALE = False
#THUMBNAIL_CACHE_TIMEOUT = 1

STATIC_ROOT = '/static/'

TINYMCE_JS_URL = '/static/lib/tinymce/3.4/tiny_mce_src.js'
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template",
    'theme': "advanced",
    'width': '80%',
    'height': '350px',
    'theme_advanced_toolbar_location': "top",
    'theme_advanced_toolbar_align': "left",
    'theme_advanced_statusbar_location': "bottom",
#    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    'entities': "160,nbsp,38,amp,34,quot,162,cent,8364,euro,163,pound,165,yen,169,copy,174,reg,8482,trade,8240,permil,60,lt,62,gt,8804,le,8805,ge,176,deg,8722,minus",
    'theme_advanced_buttons1': "save,newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,styleselect,formatselect,fontselect,fontsizeselect",
    'theme_advanced_buttons2': "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,image,cleanup,help,code,|,insertdate,inserttime,preview,|,forecolor,backcolor",
    'theme_advanced_buttons3': "tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,media,advhr,|,print,|,ltr,rtl,|,fullscreen",
#    'theme_advanced_resizing': False,
    'content_css': "/static/lib/webcms/css/editor.css",
}

#TINYMCE_SPELLCHECKER = True
#TINYMCE_COMPRESSOR = True

ROSETTA_MESSAGES_PER_PAGE = 100
ROSETTA_WSGI_AUTO_RELOAD = True

ENABLE_TRANSLATION_SUGGESTIONS = True

BING_APP_ID = 'A348863A07169DAD0AC8F7D2A1964141305AB458'

EXTRA_INSTALLED_APPS = (

    'admin_tools.menu',
    'rosetta',

    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.comments',
    'django.contrib.messages',
    'django.contrib.redirects',
    'django.contrib.markup',

    'dajaxice',
    'dajax',
    'tinymce',
    'ajax_select',

    'feincms',
    'feincms.module.page',

#    'django_statsd',
    'reversion',
    'keyedcache',
    'livesettings',
    'l10n',

    'django_assets',
    'django_extensions',
    'mptt',
#    'south',
    'registration',
    'pagination',
    'sorl.thumbnail',
    'uni_form',
    'tagging',
    'haystack',
    'disqus',
    'typogrify',
    'analytical',
)

if RAVEN:
    EXTRA_INSTALLED_APPS = EXTRA_INSTALLED_APPS + (
        'raven.contrib.django.raven_compat',
    )

USE_ETAGS = True

ACCOUNT_ACTIVATION_DAYS = 7

#BLOG_COMMENTS = ''
BLOG_LIST_PAGINATION = 10

BLOG_REGIONS = (
    ('main', 'Main content'),
    ('preview', 'Content preview'),
)

ASSETS_DEBUG = True

AUTHENTICATION_BACKENDS = (
    'webcms.utils.auth.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

STATSD_HOST = "217.28.91.6"

STATSD_PORT = 8125

STATSD_SAMPLE_RATE = "1.0"

STATSD_TRACK_MIDDLEWARE = True

#AJAX_LOOKUP_CHANNELS = {
#    pass a dict with the model and the field to search against
#    'file'  : {'model':'example.person', 'search_field':'name'}
#}
# magically include jqueryUI/js/css
AJAX_SELECT_BOOTSTRAP = True
AJAX_SELECT_INLINES = 'inline'

if RAVEN:

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
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
            'sentry': {
                'level': 'ERROR',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            },
        },
    }