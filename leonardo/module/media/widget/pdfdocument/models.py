# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from leonardo.fields import SimpleSelect2Widget
from leonardo.module.media.fields import DocumentField
from leonardo.module.web.models import Widget
from leonardo.module.web.widgets.forms import WidgetUpdateForm


class DocumentForm(WidgetUpdateForm):

    file = DocumentField(widget=SimpleSelect2Widget())


class PdfDocumentWidget(Widget):

    feincms_item_editor_form = DocumentForm

    icon = "fa fa-file-pdf-o"

    file = models.ForeignKey("media.Document", verbose_name=_(
        "pdf document"), related_name="%(app_label)s_%(class)s_related")
    height = models.CharField(
        max_length=255, verbose_name=_("height"), blank=True)
    width = models.CharField(
        max_length=255, verbose_name=_("width"), blank=True)

    class Meta:
        abstract = True
        verbose_name = _("pdf document")
        verbose_name_plural = _('pdf documents')
