
from django.apps import AppConfig

from .widget import *
from django.utils.translation import ugettext_lazy as _


default_app_config = 'leonardo.module.media.MediaConfig'


class Default(object):

    @property
    def optgroup(self):
        return ('Media')

    @property
    def apps(self):
        return [
            'leonardo.module',
            'leonardo.module.media',
            'filer',
        ]

    @property
    def widgets(self):
        return [
            DownloadListWidget,
            DownloadItemWidget,
            InternetVideoWidget,
            MediaGalleryWidget,
            SimpleImageWidget,
        ]


class MediaConfig(AppConfig, Default):
    name = 'leonardo.module.media'
    verbose_name = "Media"

default = Default()
