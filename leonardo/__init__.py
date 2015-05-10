
__import__('pkg_resources').declare_namespace(__name__)


default_app_config = 'leonardo.apps.LeonardoConfig'


class Default(object):

    core = ['web', 'nav', 'media', 'search']

    @property
    def middlewares(self):
        MIDDLEWARE_CLASSES = []
        import django
        if django.VERSION >= (1, 8, 0):
            MIDDLEWARE_CLASSES += [
                'django.contrib.auth.middleware.SessionAuthenticationMiddleware']
        else:
            MIDDLEWARE_CLASSES += ['django.middleware.doc.XViewMiddleware']

        try:
            import debug_toolbar
            MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware']
        except ImportError:
            pass

        return MIDDLEWARE_CLASSES + [
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            'django.middleware.locale.LocaleMiddleware',

            # horizon
            'leonardo.middleware.HorizonMiddleware',
        ]

    @property
    def apps(self):
        return [
            'django',

            'bootstrap_admin',  # theme
            'bootstrap_admin_feincms',  # theme

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
            'compressor',

            'horizon',
            'horizon_contrib',

            'leonardo',

        ]

    @property
    def context_processors(self):
        """return CORE Conent Type Processors
        """
        cp = [
            'django.contrib.auth.context_processors.auth',
            'horizon.context_processors.horizon',
            'django.contrib.messages.context_processors.messages',
        ]
        import django

        if django.VERSION[:2] < (1, 8):

            cp += [
                'django.core.context_processors.debug',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.request',
                'django.core.context_processors.static',
            ]

        else:
            cp += [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
            ]

        return cp

default = Default()
