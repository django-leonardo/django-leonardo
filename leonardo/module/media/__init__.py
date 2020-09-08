
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
            'leonardo.module.media.widget.models.DownloadListWidget',
            'leonardo.module.media.widget.models.DownloadItemWidget',
            'leonardo.module.media.widget.models.InternetVideoWidget',
            'leonardo.module.media.widget.models.MediaGalleryWidget',
            'leonardo.module.media.widget.models.SimpleImageWidget',
            'leonardo.module.media.widget.models.SimpleVideoWidget',
            'leonardo.module.media.widget.models.VectorGraphicsWidget',
            'leonardo.module.media.widget.models.PdfDocumentWidget',
            'leonardo.module.media.widget.models.FlashObjectWidget',
        ]

    plugins = [
        ('leonardo.module.media.apps.category_nested', 'List of directories'),
        ('leonardo.module.media.apps.category_simple',
         'Simple list of directories'),
    ]

    config = {
        'MEDIA_PAGINATE_BY': (25, _('Pagination count for media files')),
        'MEDIA_PUBLIC_UPLOAD_TO': ('public', _('Prefix for public files from MEDIA_ROOT')),
        'MEDIA_PRIVATE_UPLOAD_TO': ('private', _('Prefix for private files from MEDIA_ROOT')),
        'MEDIA_IS_PUBLIC_DEFAULT': (True, _('Set uploaded files to public automatically')),
        'MEDIA_GALLERIES_ROOT': ('', _("Used as root for navigation extensions and external app.")),
        'MEDIA_ENABLE_PERMISSIONS': (True, _(
            'Permissions for downloadable items. Experimental feature.')),
        'MEDIA_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS': (False, _('ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS')),
        'MEDIA_THUMB_SMALL_GEOM': ('64x64', _('MEDIA_THUMB_SMALL_GEOM')),
        'MEDIA_THUMB_SMALL_OPT': ('', _('Another options for small thumnails')),
        'MEDIA_THUMB_MEDIUM_GEOM': ('356x190', _('MEDIA_THUMB_MEDIUM_GEOM')),
        'MEDIA_THUMB_MEDIUM_OPT': ('', _('Another options for medium thumnails')),
        'MEDIA_THUMB_LARGE_GEOM': ('768x768', _('MEDIA_THUMB_LARGE_GEOM')),
        'MEDIA_THUMB_LARGE_OPT': ('', _('Another options for large thumnails')),
        'MEDIA_CANONICAL_URL': ('files/', _("Contrary to the file's actual URL, the canonical URL does not change if you upload a new version of the file.")),
        'MEDIA_LIST_SHOW_DIRS': (False, _("Show dirs in nested list of directories. This expose private folders now!!")),
        'MEDIA_LIST_SHOW_TITLES': (True, _("Show image titles in directory list.")),
        'MEDIA_FILES_ORDER_BY': ('-uploaded_at', _("Field which will be used to sort files like -uploaded_at, use comma to set more")),
        'MEDIA_FOLDERS_ORDER_BY': ('-created_at', _("Field which will be used to sort folders like -created_at, use comma to set more")),
    }

    page_actions = ['media/_actions.html']


def fill_language_code_choices(sender, **kwargs):
    """
    Fills in the choices for ``language_code`` from the ``LANGUAGES`` class
    variable. This method is a receiver of Django's ``class_prepared``
    signal.
    """

    raise Exception(sender)


class MediaConfig(AppConfig, Default):
    name = 'leonardo.module.media'
    verbose_name = "Media"

    def ready(self, *args, **kwargs):
        from django.apps import apps
        ImageTranslation = apps.get_model("media", "ImageTranslation")
        ImageTranslation._prepare()

        #raise Exception(class_prepared.receivers)

default = Default()
