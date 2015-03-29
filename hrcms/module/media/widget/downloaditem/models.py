# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from webcms.models import Widget

from webcms.module.media.models import File 

class DownloadItemWidget(Widget):
    file = models.ForeignKey(File, verbose_name=_("file"))

    class Meta:
        abstract = True
        verbose_name = _("download item")
        verbose_name_plural = _('download items')
