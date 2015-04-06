

from django.apps import AppConfig

from .widget import *

default_app_config = 'leonardo.module.lang.LanConfig'


class Default(object):

    @property
    def apps(self):
        return [
            'leonardo.module.lang',
        ]

    @property
    def widgets(self):
        return [
            LanguageSelectorWidget
        ]


class LanConfig(AppConfig, Default):
    name = 'leonardo.module.lang'
    verbose_name = "Language"

    def ready(self):

        """
        from feincms.module.page.models import Page

        pre_save.connect(page_check_options, sender=Page)
        post_save.connect(test, sender=Page)
        """


default = Default()
