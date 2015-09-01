
import warnings


class Default(object):

    core = ['web', 'nav', 'media', 'search', 'devel', 'leonardo_auth']

    @property
    def middlewares(self):
        MIDDLEWARE_CLASSES = [
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.middleware.http.ConditionalGetMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'django.contrib.sites.middleware.CurrentSiteMiddleware',

        ]
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

        return MIDDLEWARE_CLASSES

    @property
    def apps(self):
        return [
            'django',

            'django_extensions',
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.staticfiles',
            'django.contrib.sitemaps',

            'rest_framework',
            'dbtemplates',

            'django_select2',

            'reversion',
            'compressor',

            'horizon',
            'horizon_contrib',

            'leonardo',

            'constance',
            'constance.backends.database',

        ]

    @property
    def context_processors(self):
        """return CORE Conent Type Processors
        """
        cp = [
            'django.contrib.auth.context_processors.auth',
            'horizon.context_processors.horizon',
            'django.contrib.messages.context_processors.messages',

            'constance.context_processors.config',
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


class Leonardo(object):

    default = default

    def get_all_modules(self):
        from leonardo.utils.settings import get_leonardo_modules
        return get_leonardo_modules

    def get_app_modules(self, apps):
        """return array of imported leonardo modules for apps
        """
        from django.utils.importlib import import_module
        from django.utils.module_loading import module_has_submodule
        modules = []

        # Try importing a modules from the module package
        package_string = '.'.join(['leonardo', 'module'])

        for app in apps:
            try:
                # check if is not full app
                _app = import_module(app)
            except ImportError:
                _app = False
            if not _app:
                # obsolete part
                try:
                    # check if is not leonardo_module
                    _app = import_module('leonardo_module_{}'.format(app))
                except ImportError:
                    _app = False

            if module_has_submodule(import_module(package_string), app) or _app:
                if _app:
                    mod = _app
                else:
                    mod = import_module('.{0}'.format(app), package_string)
                modules.append(mod)
            else:
                warnings.warn('%s was skipped because app was '
                              'not found in PYTHONPATH' % app,
                              ImportWarning)
        return modules

leonardo = Leonardo()
