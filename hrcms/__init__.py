
default_app_config = 'hrcms.apps.HRCMSAppConfig'

VERSION = (0, 1, 1,)
__version__ = '.'.join(map(str, VERSION))

class Default(object):

    @property
    def middlewares(self):
        return [
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.middleware.locale.LocaleMiddleware',

            # horizon
            'hrcms.middleware.HorizonMiddleware',
            'hrcms.middleware.LeonardoMiddleware',
        ]

    @property
    def apps(self):
        return [
            'django',

            # admin tools
            #'admin_tools',
            #'admin_tools.theming',
            #'admin_tools.menu',
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

            'django_select2',

            'livesettings',

            'reversion',

            'horizon',
            'compressor',
            'hrcms',
            'horizon_contrib',
            # filer
            'filer',
            'easy_thumbnails',

            'project',
        ]

    @property
    def ctp(self):
        """return CORE Conent Type Processors
        """
        return [
            'django.contrib.auth.context_processors.auth',
            'django.core.context_processors.debug',
            'django.core.context_processors.i18n',
            'django.core.context_processors.media',
            'django.core.context_processors.request',
            'django.core.context_processors.static',
            # horizon
            'horizon.context_processors.horizon',
            'hrcms.module.web.processors.add_page_if_missing',
        ]

default = Default()


def merge(a, b):
    return list(a) + list(b)
