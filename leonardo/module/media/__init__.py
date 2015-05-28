
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
        ]

    @property
    def widgets(self):
        return [
            DownloadListWidget,
            DownloadItemWidget,
            InternetVideoWidget,
            MediaGalleryWidget,
            SimpleImageWidget,
            VectorGraphicsWidget,
            PdfDocumentWidget,
            FlashObjectWidget,
        ]

    plugins = [
        ('leonardo.module.media.apps.category_nested', 'List of directories'),
        ('leonardo.module.media.apps.category_simple', 'Simple list of directories'),
    ]


class MediaConfig(AppConfig, Default):
    name = 'leonardo.module.media'
    verbose_name = "Media"

default = Default()
