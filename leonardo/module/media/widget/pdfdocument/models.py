# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from webcms.models import Widget

from webcms.module.media.models import File 

class PdfDocumentWidget(Widget):
    file = models.ForeignKey(File, verbose_name=_("pdf document"), limit_choices_to={'type': 'pdf'})
    height = models.CharField(max_length=255, verbose_name=_("height"), blank=True)
    width = models.CharField(max_length=255, verbose_name=_("width"), blank=True)

    class Meta:
        abstract = True
        verbose_name = _("pdf document")
        verbose_name_plural = _('pdf documents')
