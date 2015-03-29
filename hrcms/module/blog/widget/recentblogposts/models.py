# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from webcms.models import Widget

from elephantblog.models import Entry

class RecentBlogPostsWidget(Widget):
    post_count = models.PositiveIntegerField(verbose_name=_("post count"), default=3)
    show_button = models.BooleanField(default=True, verbose_name=_("show link button"))

    def get_last_posts(self):
        return Entry.objects.filter(published__gt=40).order_by('-published_on')[:self.post_count]

    def get_all_posts(self):
        return Entry.objects.filter(published__in=[50,60]).order_by('-published_on')

    class Meta:
        abstract = True
        verbose_name = _("recent blog posts")
        verbose_name_plural = _("recent blog posts")
