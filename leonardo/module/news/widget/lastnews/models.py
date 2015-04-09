# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from leonardo.module.web.models import Widget

from leonardo.module.news.models import NewsEntry


class LastNewsWidget(Widget):
    news_count = models.PositiveIntegerField(
        verbose_name=_("news count"), default=2)
    show_archive_button = models.BooleanField(
        default=True, verbose_name=_("show archive button"))

    def get_last_news(self):
        return NewsEntry.objects.filter(published=True).order_by('-published_on')[:self.news_count]

    class Meta:
        abstract = True
        verbose_name = _("last news")
        verbose_name_plural = _("last news")
