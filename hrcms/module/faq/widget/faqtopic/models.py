# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from webcms.models import Widget

from webcms.module.faq.models import FaqCategory

class FaqTopicWidget(Widget):
    category = models.ForeignKey(FaqCategory, verbose_name=_("FAQ topic"))

    class Meta:
        abstract = True
        verbose_name = _("FAQ topic")
        verbose_name_plural = _("FAQ topics")
