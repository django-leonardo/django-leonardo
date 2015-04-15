
default_app_config = 'leonardo.apps.LeonardoConfig'

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
            'leonardo.middleware.HorizonMiddleware',
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
            'dbtemplates',

            'django_select2',

            'reversion',

            'horizon',
            'compressor',
            'leonardo',
            'horizon_contrib',
            'filer',
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
        ]

default = Default()


def merge(a, b):
    """return merged tuples or lists without duplicates
    """
    _a = list(a)
    for x in list(b):
        if x not in _a:
            _a.append(x)
    return _a
