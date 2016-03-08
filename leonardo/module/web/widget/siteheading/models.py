# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.template.context import RequestContext
from django.conf import settings
from leonardo.module.web.models import Widget
from .forms import SiteHeadingForm


class SiteHeadingWidget(Widget):

    feincms_item_editor_form = SiteHeadingForm

    icon = "fa fa-text-width"

    site_title = models.CharField(
        max_length=255, verbose_name=_("Site Title"), null=True, blank=True)
    logo = models.ForeignKey('media.Image',
                             blank=True, null=True, verbose_name=_("Logo"), related_name="%(app_label)s_%(class)s_images")

    tagline = models.TextField(blank=True, verbose_name=_("Tagline"))

    def get_template_data(self, request):

        if not self.site_title:
            self.site_title = settings.META_TITLE

        return {}

    class Meta:
        abstract = True
        verbose_name = _("site heading")
        verbose_name_plural = _('site headings')
