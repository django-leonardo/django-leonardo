# -#- coding: utf-8 -#-

import feedparser

from django.db import models
from django.utils.translation import ugettext_lazy as _
from leonardo.module.web.models import ContentProxyWidgetMixin
from leonardo.module.web.models import Widget
from leonardo.module.web.widgets.mixins import JSONContentMixin
from leonardo.module.web.widgets.mixins import ListWidgetMixin


class FeedReaderWidget(Widget, JSONContentMixin, ContentProxyWidgetMixin,
                       ListWidgetMixin):

    max_items = models.IntegerField(_('max. items'), default=5)

    class Meta:
        abstract = True
        verbose_name = _("feed reader")
        verbose_name_plural = _('feed readers')

    def update_cache_data(self, save=True):
        pass

    def get_data(self):

        feed = feedparser.parse(self.source_address)
        entries = feed['entries'][:self.max_items]

        return entries
