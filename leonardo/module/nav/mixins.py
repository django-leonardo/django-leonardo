

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

ORIENTATION_CHOICES = (
    ('vertical', 'Vertical'),
    ('horizon', 'Horizon'),
)


class NavigationWidgetMixin(models.Model):

    display_active = models.NullBooleanField(
        verbose_name=_('Display active'), default=True)

    display_in_nav = models.NullBooleanField(
        verbose_name=_('Display in navigation'), default=True)

    orientation = models.CharField(
        verbose_name=_("Orientation"), max_length=20,
        choices=ORIENTATION_CHOICES, default='horizontal')

    class Meta:
        abstract = True
