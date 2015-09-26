# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from leonardo.module.web.models import ListWidget
from leonardo.fields import SimpleSelect2Widget
from leonardo.module.media.fields.folder import FolderField
from leonardo.module.web.widgets.forms import WidgetUpdateForm


class FolderForm(WidgetUpdateForm):

    folder = FolderField(widget=SimpleSelect2Widget())


class DownloadListWidget(ListWidget):

    icon = "fa fa-list-alt"

    feincms_item_editor_form = FolderForm

    folder = models.ForeignKey('media.Folder', verbose_name=_(
        "folder"), related_name="%(app_label)s_%(class)s_folders")

    class Meta:
        abstract = True
        verbose_name = _("download list")
        verbose_name_plural = _('download lists')
