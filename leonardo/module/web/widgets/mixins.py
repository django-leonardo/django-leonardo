

from __future__ import unicode_literals

from django.utils import timezone
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .const import PAGINATION_CHOICES


class ListWidgetMixin(models.Model):

    """Common fields for object lists
    """

    objects_per_page = models.PositiveIntegerField(
        verbose_name=_('Objects per page'), blank=True, default=6)

    objects_per_row = models.PositiveIntegerField(
        verbose_name=_('Objects per row'), blank=True, default=3)

    pagination_style = models.CharField(
        verbose_name=_("Pagination Style"), max_length=50,
        choices=PAGINATION_CHOICES, default='paginator')

    class Meta:
        abstract = True


class ContentProxyWidgetMixin(models.Model):

    """Content proxy widget mixin
    """

    source_address = models.CharField(
        verbose_name=_("Source Address"), max_length=255)

    cache_validity = models.PositiveIntegerField(
        verbose_name=_('Cache validity'), default=3600)

    cache_data = models.TextField(
        verbose_name=_("Cache data"), blank=True)

    cache_updated = models.DateTimeField(
        verbose_name=_('Cache update'),
        editable=False, null=True, blank=True)

    def is_obsolete(self):
        """returns True is data is obsolete and needs revalidation
        """
        if self.cache_updated:
            now = timezone.now()
            delta = now - self.cache_updated
            if delta.seconds > self.cache_validity:
                return True
        else:
            return True
        return False

    def update_cache(self, data=None):
        """call after set data to self.cache_data or provide cached data
        1. set your data to self.cache_data
        2. call this method without saving the instance
        """
        if data:
            self.cache_data = data
        self.cache_updated = timezone.now()
        self.save()

    class Meta:
        abstract = True


class AuthContentProxyWidgetMixin(models.Model):

    """widget mixin for getting remote content with credentials
    """

    username = models.CharField(
        verbose_name=_("Username"), max_length=255, blank=True, null=True)

    password = models.CharField(
        verbose_name=_('Password'), max_length=255, blank=True, null=True)

    token = models.CharField(
        verbose_name=_('API Token'), max_length=255, blank=True, null=True)

    class Meta:
        abstract = True
