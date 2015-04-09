
from django.apps import AppConfig


default_app_config = 'leonardo.module.news.NewsConfig'

from .widget import *


class Default(object):

    optgroup = ('News')

    @property
    def apps(self):
        return [
            'leonardo.module.news',
        ]

    @property
    def widgets(self):
        return [
            LastNewsWidget
        ]


class NewsConfig(AppConfig, Default):
    name = 'leonardo.module.news'
    verbose_name = "News"


default = Default()
