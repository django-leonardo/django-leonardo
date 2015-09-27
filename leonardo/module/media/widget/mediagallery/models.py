# -#- coding: utf-8 -#-

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from leonardo.fields import SimpleSelect2Widget
from leonardo.module.media.fields.folder import FolderField
from leonardo.module.web.models import ListWidget
from leonardo.module.web.widgets.forms import WidgetUpdateForm

DETAIL_CHOICES = (
    ('open_modal', _('open in modal window')),
    ('open_new_window', _('open new window')),
    ('on_page', _('disply in page')),
)

SIZE_CHOICES = (
    ('small', _('small')),
    ('medium', _('medium')),
    ('large', _('large')),
)


class FolderForm(WidgetUpdateForm):

    folder = FolderField(widget=SimpleSelect2Widget())


class MediaGalleryWidget(ListWidget):

    feincms_item_editor_form = FolderForm

    icon = "fa fa-picture-o"

    folder = models.ForeignKey('media.Folder', verbose_name=_(
        "Directory"), related_name="%(app_label)s_%(class)s_folders")
    size = models.CharField(max_length=255, verbose_name=_(
        "thumbnail size"), choices=SIZE_CHOICES, default='small')
    detail = models.CharField(max_length=255, verbose_name=_(
        "detail view"), choices=DETAIL_CHOICES, default='modal')

    def thumb_geom(self):
        return getattr(settings,
                       'MEDIA_THUMB_%s_GEOM' % self.size.upper(),
                       '96x96')

    def image_geom(self):
        return '800x800'

    class Meta:
        abstract = True
        verbose_name = _("media gallery")
        verbose_name_plural = _('media galleries')
