# -#- coding: utf-8 -#-

import datetime

import feedparser
from django.db import models
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from hrcms.models import Widget

TARGET_CHOICES = (
    ('modal', _('Modal window')),
    ('blank', _('Blank window')),
)


class FeedReaderWidget(Widget):
    link = models.URLField(_('link'))
    cached_content = models.TextField(blank=True, editable=False)
    max_items = models.IntegerField(_('max. items'), default=5)
    last_updated = models.DateTimeField(
        _('last updated'), blank=True, null=True, editable=False)

    class Meta:
        abstract = True
        verbose_name = _("feed reader")
        verbose_name_plural = _('feed readers')

    def render_content(self, options):

        regen = False
        if self.last_updated:
            now = datetime.datetime.now()
            delta = now - self.last_updated
            if delta.seconds > 3600:
                regen = True
        else:
            regen = True

        if regen:
            self.cache_content(None, True)

        context = RequestContext(options.get('request'), {
            'widget': self,
        })

        return render_to_string(self.template_name, context)

    def cache_content(self, date_format=None, save=True):

        feed = feedparser.parse(self.link)
        entries = feed['entries'][:self.max_items]
        if date_format:
            for entry in entries:
                entry.updated = time.strftime(
                    date_format, entry.updated_parsed)

        context = {
            'widget': self,
            'link': feed['feed']['link'],
            'entries': entries,
        }

        self.cached_content = render_to_string(
            'widget/feedreader/_content.html', context)
        self.last_updated = datetime.datetime.now()

        if save:
            self.save()

    def save(self, *args, **kwargs):
        self.cache_content(None, False)
        super(FeedReaderWidget, self).save(*args, **kwargs)
