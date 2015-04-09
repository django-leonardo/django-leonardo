
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from .widget import *


default_app_config = 'leonardo.module.blog.BlogConfig'


class Default(object):

    optgroup = ('Blog')

    @property
    def middlewares(self):
        return [
            'leonardo.module.web.middleware.WebMiddleware',
        ]

    @property
    def apps(self):
        return [
            'elephantblog',
            'leonardo.module.blog',

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
            BlogCategoriesWidget,
            RecentBlogPostsWidget,
        ]

    @property
    def plugins(self):
        return [
            ('elephantblog.urls', 'Blog'),
        ]


class BlogConfig(AppConfig, Default):
    name = 'leonardo.module.blog'
    verbose_name = "Blog"

    def ready(self):
        """
        from feincms.module.page.models import Page

        pre_save.connect(page_check_options, sender=Page)
        post_save.connect(test, sender=Page)
        """

default = Default()
