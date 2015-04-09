
from django.apps import AppConfig

from .widget import *


default_app_config = 'leonardo.module.web.WebConfig'


class Default(object):

    @property
    def middlewares(self):
        return [
            'leonardo.module.web.middleware.WebMiddleware',
        ]

    @property
    def apps(self):
        return [
            'markitup',
            'feincms',
            'mptt',
            'crispy_forms',

            'leonardo.module',

            'feincms.module.page',
            'feincms.content.application',
            #'feincms.content.comments',

            'leonardo.module.nav',
            'leonardo.module.lang',
            'leonardo.module.forms',
            'leonardo.module.web',
            #'hrcms.module.forms',
            #'hrcms.module.boardie',
            'form_designer',
            'django_remote_forms',
        ]

    @property
    def ctp(self):
        """return WEB Conent Type Processors
        """
        return [
            'leonardo.module.web.processors.add_page_if_missing',
        ]

    @property
    def widgets(self):
        return [
            ApplicationWidget,
            SiteHeadingWidget,
            MarkupTextWidget,
            FeedReaderWidget,
            HtmlTextWidget,
        ]


class WebConfig(AppConfig, Default):
    name = 'leonardo.module.web'
    verbose_name = "CMS"

    def ready(self):
        """
        from feincms.module.page.models import Page

        pre_save.connect(page_check_options, sender=Page)
        post_save.connect(test, sender=Page)
        """

default = Default()
