# -#- coding: utf-8 -#-

import datetime

import feedparser
from django.db import models
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from leonardo.module.web.models import Widget, ContentProxyWidgetMixin
from leonardo.module.web.widgets.mixins import ListWidgetMixin

TARGET_CHOICES = (
    ('modal', _('Modal window')),
    ('blank', _('Blank window')),
)


class FeedReaderWidget(Widget, ContentProxyWidgetMixin, ListWidgetMixin):
    max_items = models.IntegerField(_('max. items'), default=5)

    class Meta:
        abstract = True
        verbose_name = _("feed reader")
        verbose_name_plural = _('feed readers')

    def render_content(self, options):

        if self.is_obsolete:
            self.update_cache_data()

        context = RequestContext(options.get('request'), {
            'widget': self,
        })

        return render_to_string(self.get_template_name(), context)

    def update_cache_data(self, save=True):

        feed = feedparser.parse(self.link)
        entries = feed['entries'][:self.max_items]

        context = {
            'widget': self,
            'link': feed['feed']['link'],
            'entries': entries,
        }

        self.cache_data = render_to_string(
            'widget/feedreader/_content.html', context)
        self.cache_update = datetime.datetime.now()

        if save:
            self.save()

    def save(self, *args, **kwargs):
        self.update_cache_data(False)
        super(FeedReaderWidget, self).save(*args, **kwargs)
