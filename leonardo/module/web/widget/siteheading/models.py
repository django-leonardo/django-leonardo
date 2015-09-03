# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.template.context import RequestContext
from django.conf import settings
from leonardo.module.web.models import Widget


class SiteHeadingWidget(Widget):

    icon = "fa fa-text-width"

    site_title = models.CharField(
        max_length=255, verbose_name=_("Site Title"), null=True, blank=True)
    logo = models.ForeignKey('media.Image',
                             blank=True, null=True, verbose_name=_("Logo"), related_name="%(app_label)s_%(class)s_images")

    tagline = models.TextField(blank=True, verbose_name=_("Tagline"))

    def render_content(self, options):

        if not self.site_title:
            self.site_title = settings.META_TITLE

        context = RequestContext(options.get('request'), {
            'widget': self,
        })

        return render_to_string(self.get_template_name(), context)

    class Meta:
        abstract = True
        verbose_name = _("site heading")
        verbose_name_plural = _('site headings')
