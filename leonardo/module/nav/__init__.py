
from django.apps import AppConfig

from .widget import *


default_app_config = 'leonardo.module.nav.NavConfig'


class Default(object):

    optgroup = ('Navigation')

    apps = ['leonardo.module.nav']

    @property
    def widgets(self):
        return [
            TreeNavigationWidget,
            ContentNavigationWidget,
            ContextNavigationWidget,
            LinearNavigationWidget,
            BreadcrumbsWidget,
            SiteMapWidget,
            SiteSearchWidget,
            LanguageSelectorWidget
        ]


class NavConfig(AppConfig, Default):
    name = 'leonardo.module.nav'
    verbose_name = "Navigation Module"

default = Default()
