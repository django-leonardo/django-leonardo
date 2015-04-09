
from django.apps import AppConfig

from .widget import *


default_app_config = 'leonardo.module.nav.NavConfig'


class Default(object):

    optgroup = ('Navigation')

    @property
    def apps(self):
        return [
            'leonardo.module.nav'
        ]

    @property
    def widgets(self):
        return [
            TreeNavigationWidget,
            ContentNavigationWidget,
            ContextNavigationWidget,
            LinearNavigationWidget,
            BreadcrumbsWidget,
            SiteMapWidget,
            SiteSearchWidget
        ]


class NavConfig(AppConfig, Default):
    name = 'leonardo.module.nav'
    verbose_name = "Navigation Module"

    def ready(self):

        """
        from feincms.module.page.models import Page

        pre_save.connect(page_check_options, sender=Page)
        post_save.connect(test, sender=Page)
        """


default = Default()
