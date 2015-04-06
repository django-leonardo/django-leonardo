# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from webcms.models import Widget

from webcms.module.media.models import Category 

class DownloadListWidget(Widget):
    category = models.ForeignKey(Category, verbose_name=_("files"))

    class Meta:
        abstract = True
        verbose_name = _("download list")
        verbose_name_plural = _('download lists')
