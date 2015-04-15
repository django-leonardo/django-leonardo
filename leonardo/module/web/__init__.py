
from django.apps import AppConfig

from .widget import *


default_app_config = 'leonardo.module.web.WebConfig'


class Default(object):

    optgroup = 'Web'

    @property
    def middlewares(self):
        return [
            'leonardo.module.web.middleware.WebMiddleware',
        ]

    @property
    def apps(self):
        return [
            'feincms',
            'mptt',
            'crispy_forms',
            'dbtemplates',
            'leonardo.module',
            'easy_thumbnails',

            'feincms.module.page', # noqa

            'leonardo.module.web',

            'markupfield',

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
            PageTitleWidget,
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
