# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.utils.translation import get_language_from_request
from leonardo.module.nav.forms import NavigationForm
from django.utils.functional import cached_property

from leonardo.module.web.models import Widget, Page


class SiteMapWidget(Widget):

    feincms_item_editor_form = NavigationForm

    root = models.ForeignKey(Page, blank=True, null=True, verbose_name=_(
        "Root page"), related_name="sitemap_root", help_text=_("If no root page is set, widget's parent page will be used."))

    class Meta:
        abstract = True
        verbose_name = _("Site map")
        verbose_name_plural = _('Site maps')

    @cached_property
    def get_root(self):
        return self.root if self.root else self.parent

    def render_content(self, options):
        request = options['request']
        page_list = self.root.get_children()

        return render_to_string(self.get_template_name(), {
            'widget': self,
            'page_list': page_list,
            'request': request,
        })
