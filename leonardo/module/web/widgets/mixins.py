

from __future__ import unicode_literals

import json
import datetime
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from .const import PAGINATION_CHOICES

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


class ListModelMixin(models.Model):
    """Common fields for list functionality
    """

    objects_per_page = models.PositiveIntegerField(
        verbose_name=_('Objects per page'), blank=True, default=6)

    objects_per_row = models.PositiveIntegerField(
        verbose_name=_('Objects per row'), blank=True, default=3)

    pagination_style = models.CharField(
        verbose_name=_("Pagination Style"), max_length=50,
        choices=PAGINATION_CHOICES, default='paginator')

    tabs = {
        'pagination': {
            'name': _('Pagination'),
            'fields': ('objects_per_page',
                       'objects_per_row',
                       'pagination_style')
        }
    }

    class Meta:
        abstract = True


class ListMixin(object):

    """Basic object list implementation

    1. declare get_items which returns all objects
    2. if you want filtering data make this in filter_items(items)
    3. if you want get data in template use items property or
    get_rows or get_pages which has sorted items to pages and rows by settings

    note: this mixin could be used without model but is limited to default
    pagination
    """

    objects_per_page = 25
    objects_per_row = 3
    pagination_style = "paginator"

    def get_items(self, request=None):
        '''returns queryset or array of items for listing'''
        raise NotImplementedError('ListWidget must has get_items method')

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
    def get_rows(self):
        '''returns rows with items
        [[item1 item2], [item3 item4], [item5]]'''
        rows = []
        row = []
        for i, item in enumerate(self.items):
            if i > 0 and i % self.objects_per_row == 0:
                rows.append(row)
                row = []
            row.append(item)
        rows.append(row)
        return rows

    @cached_property
    def columns_classes(self):
        '''returns columns count'''
        md = 12 / self.objects_per_row
        sm = None
        if self.objects_per_row > 2:
            sm = 12 / (self.objects_per_row / 2)
        return md, (sm or md), 12

    @cached_property
    def item_classes(self):
        '''Return all classes for every item in row
        This is specific for concrete frontend framework
        '''
        return 'col-md-{} col-xs-{} col-sm-{}'.format(self.columns_classes)

    @cached_property
    def get_pages(self):
        '''returns pages with rows'''
        pages = []
        page = []
        for i, item in enumerate(self.get_rows):
            if i > 0 and i % self.objects_per_page == 0:
                pages.append(page)
                page = []
            page.append(item)
        pages.append(page)
        return pages

    @cached_property
    def needs_pagination(self):
        """Calculate needs pagination"""
        if self.objects_per_page == 0:
            return False
        if len(self.items) > self.objects_per_page \
                or len(self.get_pages[0]) > self.objects_per_page:
            return True
        return False

    @cached_property
    def get_list_template(self):
        '''returns base list template by pagination_style'''
        return "base/widget/list/_%s.html" % self.pagination_style

    @cached_property
    def get_item_template(self):
        '''returns template for signle object from queryset
        If you have a template name my_list_template.html
        then template for a single object will be
        _my_list_template.html

        Now only for default generates _item.html
        _item.html is obsolete use _default.html
        '''
        content_template = self.content_theme.name

        # _item.html is obsolete use _default.html
        # TODO: remove this condition after all _item.html will be converted
        if content_template == "default":
            return "widget/%s/_item.html" % self.widget_name

        # TODO: support more template suffixes
        return "widget/%s/_%s.html" % (self.widget_name, content_template)

    def __init__(self, *args, **kwargs):
        super(ListMixin, self).__init__(*args, **kwargs)

        get_items = getattr(self, 'get_items', None)
        render = getattr(self, 'render', None)
        if not callable(get_items) or not callable(render):
            raise Exception('bases on ListWidgetMixin must '
                            'have implemented get_items or render method')


class ListWidgetMixin(ListModelMixin, ListMixin):

    """Provide basae for listing widgets
    """

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

    def get_items(self):
        return self.data

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

    def parse_time(self, time):
        return datetime.date(*time[:3]).isoformat()

    @property
    def data(self):
        """load and cache data in json format
        """

        if self.is_obsolete():
            data = self.get_data()
            for datum in data:
                if 'published_parsed' in datum:
                    datum['published_parsed'] = \
                        self.parse_time(datum['published_parsed'])

            try:
                dumped_data = json.dumps(data)
            except:
                self.update_cache(data)
            else:
                self.update_cache(dumped_data)
                return data

        try:
            return json.loads(self.cache_data)
        except:
            return self.cache_data

        return self.get_data()


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
