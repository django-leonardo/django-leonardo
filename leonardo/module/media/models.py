
import os
from datetime import datetime

from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.timezone import get_current_timezone, make_aware, now
from django.utils.translation import ugettext_lazy as _
from feincms.module.page.extensions.navigation import (NavigationExtension,
                                                       PagePretender)
from feincms.translations import (TranslatedObjectManager,
                                  TranslatedObjectMixin, Translation)

from filer.utils.compatibility import python_2_unicode_compatible

from .mediamodels.foldermodels import Folder, FolderPermission
from .mediamodels.imagemodels import Image
from .mediamodels.filemodels import File
from .mediamodels.clipboardmodels import Clipboard, ClipboardItem
from .mediamodels.virtualitems import *
from .mediamodels import tools


class MediaMixin(object):

    @classmethod
    def matches_file_type(cls, iname, ifile=None, request=None):
        # the extensions we'll recognise for this file type
        # (majklk): TODO move to settings or live config
        filename_extensions = getattr(cls, 'filename_extensions', '*')
        ext = os.path.splitext(iname)[1].lower()
        return ext in filename_extensions


class MediaTranslationMixin(object):

    original_filename = models.CharField(
        _('original filename'), max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, default="", blank=True,
                            verbose_name=_('name'))
    description = models.TextField(null=True, blank=True,
                                   verbose_name=_('description'))


class FolderTranslation(Translation(Folder)):

    """
    Translated Document
    """

    name = models.CharField(max_length=255, default="", blank=True,
                            verbose_name=_('name'))

    class Meta:
        verbose_name = ("Folder translation")
        verbose_name_plural = ('Folder translations')
        app_label = 'media'


class Document(MediaMixin, File):

    filename_extensions = ['.pdf', '.xls']

    class Meta:
        verbose_name = ("document")
        verbose_name_plural = ('documents')


class DocumentTranslation(Translation(Document), MediaTranslationMixin):

    """
    Translated Document
    """

    class Meta:
        verbose_name = ("document translation")
        verbose_name_plural = ('document translations')
        app_label = 'media'


class Vector(MediaMixin, File):

    filename_extensions = ['.svg', '.eps', ]

    class Meta:
        verbose_name = ("vector")
        verbose_name_plural = ('vetors')


class VectorTranslation(Translation(Vector), MediaTranslationMixin):

    """
    Translated Vector
    """

    class Meta:
        verbose_name = ("vector translation")
        verbose_name_plural = ('vector translations')
        app_label = 'media'


class Video(MediaMixin, File):

    filename_extensions = ['.dv', '.mov', '.mp4', '.avi', '.wmv', ]

    class Meta:
        verbose_name = ("video")
        verbose_name_plural = ('videos')


class VideoTranslation(Translation(Video), MediaTranslationMixin):

    """
    Translated Video
    """

    class Meta:
        verbose_name = ("video translation")
        verbose_name_plural = ('video translations')
        app_label = 'media'


class Flash(MediaMixin, File):

    filename_extensions = ['.swf']

    class Meta:
        verbose_name = ("flash video")
        verbose_name_plural = ('flash videos')


class ImageTranslation(Translation(Image)):

    name = models.CharField(max_length=255, default="", blank=True,
                            verbose_name=_('name'))
    default_alt_text = models.CharField(max_length=255, default="", blank=True,
                                        verbose_name=_('default alt text'))

    default_caption = models.CharField(max_length=255, default="", blank=True,
                                       verbose_name=_('default caption'))

    description = models.TextField(null=True, blank=True,
                                   verbose_name=_('description'))

    class Meta:
        verbose_name = ("image translation")
        verbose_name_plural = ('image translations')
        app_label = 'media'


class MediaCategoriesNavigationExtension(NavigationExtension):
    name = _('All media categories')

    def children(self, page, **kwargs):
        base_url = page.get_absolute_url()
        category_list = Folder.objects.filter(parent=None)
        for category in category_list:
            subchildren = []
            for subcategory in category.media_folder_children.all():
                subchildren.append(PagePretender(
                    title=subcategory,
                    url='%s%s/%s/' % (base_url, category.name, subcategory.name),
                    level=5
                ))
            yield PagePretender(
                title=category,
                url='%s%s/' % (base_url, category.name),
                children=subchildren,
                level=5
            )
