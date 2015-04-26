
from django.apps import AppConfig

from .widget import *


default_app_config = 'leonardo.module.media.MediaConfig'


class Default(object):

    optgroup = 'Media'

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
