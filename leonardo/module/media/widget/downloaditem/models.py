# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from leonardo.fields import SimpleSelect2Widget
from leonardo.module.media.fields import FileField
from leonardo.module.web.models import Widget
from leonardo.module.web.widgets.forms import WidgetUpdateForm


class FileForm(WidgetUpdateForm):

    file = FileField(widget=SimpleSelect2Widget())


class DownloadItemWidget(Widget):

    feincms_item_editor_form = FileForm

    icon = "fa fa-download"

    file = models.ForeignKey("media.File", verbose_name=_("file"), related_name="%(app_label)s_%(class)s_files")

    class Meta:
        abstract = True
        verbose_name = _("download item")
        verbose_name_plural = _('download items')
