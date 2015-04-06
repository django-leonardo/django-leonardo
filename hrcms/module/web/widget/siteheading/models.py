# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from hrcms.module.web.models import Widget

from webcms.module.media.models import File


class SiteHeadingWidget(Widget):
    site_title = models.CharField(max_length=255, verbose_name=_("Site Title"))
    logo = models.ForeignKey(
        File, blank=True, null=True, verbose_name=_("Logo"))
    tagline = models.TextField(blank=True, verbose_name=_("Tagline"))

    class Meta:
        abstract = True
        verbose_name = _("site heading")
        verbose_name_plural = _('site headings')
