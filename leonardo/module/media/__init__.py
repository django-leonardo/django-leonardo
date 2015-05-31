
from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _

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

    config = {
        'MEDIA_PAGINATE_BY': (25, _('Pagination count for media files')),
        'MEDIA_PUBLIC_UPLOAD_TO': ('public', _('Prefix for public files from MEDIA_ROOT')),
        'MEDIA_PRIVATE_UPLOAD_TO': ('private', _('Prefix for private files from MEDIA_ROOT')),
        'MEDIA_IS_PUBLIC_DEFAULT': (True, _('Set uploaded files to public automatically')),
        'MEDIA_ENABLE_PERMISSIONS': (True, _(
            'Permissions for downloadable items. Experimental feature.')),
        'MEDIA_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS': (False, _('ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS')),
    }


class MediaConfig(AppConfig, Default):
    name = 'leonardo.module.media'
    verbose_name = "Media"

default = Default()
