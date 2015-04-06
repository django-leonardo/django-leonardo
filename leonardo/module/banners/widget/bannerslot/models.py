# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from hrcms.models import Widget

from hrcms.module.banners.models import Slot 


class BannerSlotWidget(Widget):
    slot = models.ForeignKey(Slot, verbose_name=_("banner slot"))
    random_order = models.BooleanField(default=False, verbose_name=_("random order"))
    auto_rotate = models.BooleanField(default=False, verbose_name=_("auto rotate"))
    rotation_speed = models.PositiveIntegerField(default=2000, verbose_name=_("rotation speed"))

    class Meta:
        abstract = True
        verbose_name = _("banner slot")
        verbose_name_plural = _('banner slots')
