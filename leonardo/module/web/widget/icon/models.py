# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from leonardo.module.web.models import Widget

from .const import ICON_CHOICES, SIZE_CHOICES


class IconWidget(Widget):

    """
    Font Awesome (the fist library) Icon Widget

    * http://fortawesome.github.io/Font-Awesome/icons/
    """

    icon = models.CharField(
        max_length=255, verbose_name=_("Icon"), choices=ICON_CHOICES)

    size = models.CharField(
        max_length=255, verbose_name=_("Size"), choices=SIZE_CHOICES, default='normal')

    spin = models.BooleanField(default=False, verbose_name=_("Spin"))

    border = models.BooleanField(default=False, verbose_name=_("Border"))

    class Meta:
        abstract = True
        verbose_name = _('Icon')
        verbose_name_plural = _('Icons')
