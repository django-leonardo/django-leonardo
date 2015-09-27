

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

ORIENTATION_CHOICES = (
    ('vertical', 'Vertical'),
    ('horizon', 'Horizon'),
)


class NavigationWidgetMixin(models.Model):

    '''Common fields for Page navigation'''

    display_active = models.NullBooleanField(
        verbose_name=_('Display active'), default=True)

    display_in_nav = models.NullBooleanField(
        verbose_name=_('Display in navigation'), default=True)

    orientation = models.CharField(
        verbose_name=_("Orientation"), max_length=20,
        choices=ORIENTATION_CHOICES, default='horizontal')

    def _filter_active(self, items):
        return [item for item in items if item.active == self.display_in_nav]

    def _filter_in_nav(self, items):
        return [item for item in items if item.in_navigation == self.display_in_nav]

    def filter_items(self, items):
        '''perform filtering items by specific criteria'''
        items = self._filter_active(items)
        items = self._filter_in_nav(items)
        return items

    class Meta:
        abstract = True
