

from __future__ import unicode_literals

import json
from urlparse import urlparse

from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from .const import PAGINATION_CHOICES


class ListWidgetMixin(models.Model):

    """Provide API for listing items
    """

    objects_per_page = models.PositiveIntegerField(
        verbose_name=_('Objects per page'), blank=True, default=6)

    objects_per_row = models.PositiveIntegerField(
        verbose_name=_('Objects per row'), blank=True, default=3)

    pagination_style = models.CharField(
        verbose_name=_("Pagination Style"), max_length=50,
        choices=PAGINATION_CHOICES, default='paginator')

    def get_items(self, request=None):
        '''returns queryset or array of items for listing'''
        raise NotImplementedError

    def filter_items(self, items):
        '''perform filtering items by specific criteria'''
        return items

    def set_items(self, items):
        '''just setter for items'''
        self._items = items

    @cached_property
    def items(self):
        '''access for filtered items'''
        if hasattr(self, '_items'):
            return self.filter_items(self._items)
        self._items = self.get_items()
        return self.filter_items(self._items)

    def populate_items(self, request):
        '''populate and returns filtered items'''
        self._items = self.get_items(request)
        return self.items

    @cached_property
    def get_list_template(self):
        '''returns base list template by pagination_style'''
        return "base/widget/list/_%s.html" % self.pagination_style

    @cached_property
    def get_rows(self):
        '''returns rows with items
        [[item1 item2 item3], [item2 ]]'''
        rows = []
        row = []
        for i, item in enumerate(self.items):
            if self.objects_per_row == i:
                rows.append(row)
                row = []
            row.append(item)
        rows.append(row)
        return rows

    @cached_property
    def get_pages(self):
        '''returns pages with rows'''
        pages = []
        page = []
        for i, item in enumerate(self.get_rows):
            if self.objects_per_page == i:
                pages.append(page)
                page = []
            page.append(item)
        pages.append(page)
        return pages

    @cached_property
    def get_item_template(self):
        '''returns template for one item from queryset'''
        return "widget/%s/_item.html" % self.widget_name

    class Meta:
        abstract = True


class ContentProxyWidgetMixin(models.Model):

    """Provide basic fields and routines
    for loading and caching data from external resource

    define your implementation for getting data in ``get_data``
    and use ``data`` property in your templates
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

    @cached_property
    def address_parser(self):
        return urlparse(self.source_address)

    @cached_property
    def get_port(self):
        """returns parsed port from ``source_address``
        """
        return self.address_parser.port

    @cached_property
    def get_host(self):
        """returns parsed host from ``source_address``
        """
        return self.address_parser.hostname

    def is_obsolete(self):
        """returns True is data is obsolete and needs revalidation
        """
        if self.cache_updated:
            now = timezone.now()
            delta = now - self.cache_updated
            if delta.seconds < self.cache_validity:
                return False
        return True

    def update_cache(self, data=None):
        """call with new data or set data to self.cache_data and call this
        """
        if data:
            self.cache_data = data
        self.cache_updated = timezone.now()
        self.save()

    def get_data(self, *args, **kwargs):
        """define your behavior for loading raw data
        """
        raise NotImplementedError

    @property
    def data(self):
        """this property just calls ``get_data``
        but here you can serilalize your data or render as html
        these data will be saved to self.cached_content
        also will be accessable from template
        """
        if self.is_obsolete():
            self.update_cache(self.get_data())
        return self.cache_data

    class Meta:
        abstract = True


class JSONContentMixin(object):

    """just expect json data from ``get_data`` method
    """

    @property
    def data(self):
        """load and cache data in json format
        """

        if self.is_obsolete():
            self.cache_data = json.dumps(self.get_data())
            self.update_cache()
        return json.loads(self.cache_data)


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
