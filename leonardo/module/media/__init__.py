
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

    def ready(self):

        from filer import models as filer_models
        from .models import LeonardoFolder
        filer_models.Folder = LeonardoFolder

        from filer.fields import folder
        folder.FilerFolderField.default_model_class = LeonardoFolder

default = Default()
