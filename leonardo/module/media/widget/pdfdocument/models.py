# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from leonardo.module.web.models import Widget


class PdfDocumentWidget(Widget):
    file = models.ForeignKey("media.Document", verbose_name=_(
        "pdf document"))
    height = models.CharField(
        max_length=255, verbose_name=_("height"), blank=True)
    width = models.CharField(
        max_length=255, verbose_name=_("width"), blank=True)

    class Meta:
        abstract = True
        verbose_name = _("pdf document")
        verbose_name_plural = _('pdf documents')
