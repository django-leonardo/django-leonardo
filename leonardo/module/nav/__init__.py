
from django.apps import AppConfig

default_app_config = 'leonardo.module.nav.NavConfig'


class Default(object):

    optgroup = ('Navigation')

    apps = ['leonardo.module.nav']

    @property
    def widgets(self):
        return [
            'leonardo.module.nav.models.TreeNavigationWidget',
            'leonardo.module.nav.models.ContentNavigationWidget',
            'leonardo.module.nav.models.ContextNavigationWidget',
            'leonardo.module.nav.models.LinearNavigationWidget',
            'leonardo.module.nav.models.BreadcrumbsWidget',
            'leonardo.module.nav.models.SiteMapWidget',
            'leonardo.module.nav.models.SiteSearchWidget',
            'leonardo.module.nav.models.LanguageSelectorWidget'
        ]


class NavConfig(AppConfig, Default):
    name = 'leonardo.module.nav'
    verbose_name = "Navigation Module"

default = Default()
