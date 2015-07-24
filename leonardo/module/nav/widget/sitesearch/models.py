# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from leonardo.module.web.models import Widget

ENGINE_CHOICES = (
    ('gooole', _("Google Custom Search")),
    ('haystack', _("Django Haystack")),
)


class SiteSearchWidget(Widget):
    engine = models.CharField(
        max_length=255, verbose_name=_("Search engine"),
        choices=ENGINE_CHOICES, default="google")

    class Meta:
        abstract = True
        verbose_name = _("Site search")
        verbose_name_plural = _("Site searches")
