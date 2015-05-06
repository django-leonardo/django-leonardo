
import logging
from django.apps import AppConfig

from .widget import *


default_app_config = 'leonardo.module.web.WebConfig'

LOG = logging.getLogger(__name__)


class Default(object):

    optgroup = 'Web'

    urls_conf = 'leonardo.module.web.urls'

    @property
    def middlewares(self):
        return [
            'leonardo.module.web.middleware.WebMiddleware',
        ]

    @property
    def themes(self):
        """supported themes
        """
        return ['leonardo_theme_adminlte', 'leonardo_theme_bootswatch']

    @property
    def apps(self):

        INSTALLED_APPS = []
        for theme in self.themes:
            try:
                __import__(theme)
                INSTALLED_APPS += [theme]
            except ImportError:
                LOG.warning("you are missing available theme {}".format(theme))

        try:
            import sorl  # noqa
            INSTALLED_APPS += ['sorl.thumbnail']
        except Exception:
            pass

        try:
            import easy_thumbnails  # noqa
            INSTALLED_APPS += ['easy_thumbnails']
        except Exception:
            pass

        return INSTALLED_APPS + [
            'feincms',
            'mptt',
            'crispy_forms',
            'floppyforms',

            'dbtemplates',
            'leonardo.module',

            'feincms.module.page',  # noqa

            'leonardo.module.web',

            'markupfield',
            'redactor',

        ]

    @property
    def context_processors(self):
        """return WEB Conent Type Processors
        """
        return [
            'leonardo.module.web.processors.page.add_page_if_missing',
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
            UserLoginWidget,
            UserRegistrationWidget,
        ]


class WebConfig(AppConfig, Default):
    name = 'leonardo.module.web'
    verbose_name = "CMS"

    def ready(self):

        pass

default = Default()
