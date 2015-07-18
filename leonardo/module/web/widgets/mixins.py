

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .const import PAGINATION_CHOICES


class ListWidgetMixin(object):

    """Common fields for object lists
    """

    objects_per_page = models.PositiveIntegerField(
        verbose_name=_('Objects per page'), blank=True)

    objects_per_row = models.PositiveIntegerField(
        verbose_name=_('Objects per row'), blank=True)

    pagination = models.CharField(
        verbose_name=_("Pagination"), max_length=50,
        choices=PAGINATION_CHOICES, default='paginator')

    pagination_style = models.CharField(
        verbose_name=_("Pagination Style"), max_length=50,
        choices=PAGINATION_CHOICES, default='paginator')


class ContentProxyWidgetMixin(object):

    """Content proxy widget mixin
    """

    source_address = models.CharField(
        verbose_name=_("Source Address"), max_length=255)

    cache_validity = models.PositiveIntegerField(
        verbose_name=_('Cache validity'), default=3600)

    cache_update = models.PositiveIntegerField(
        verbose_name=_('Cache update'), editable=False)

    cache_data = models.TextField(
        verbose_name=_("Cache data"), blank=True)
