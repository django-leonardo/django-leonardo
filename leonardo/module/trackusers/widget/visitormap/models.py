# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from webcms.models import Widget

class VisitorMapWidget(Widget):

    class Meta:
        abstract = True
        verbose_name = _("visitor map")
        verbose_name_plural = _('visitor maps')
