# -#- coding: utf-8 -#-

from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from leonardo.module.web.models import Page, Widget


class PageTitleWidget(Widget):

    class Meta:
        abstract = True
        verbose_name = _("page title")
        verbose_name_plural = _('page titles')

    def render_content(self, options):
        page = self.parent

        try:
            fragments = options['request']._feincms_fragments
        except:
            fragments = {}

        title = fragments.get("_page_title", None)
        subtitle = fragments.get("_page_subtitle", None)

        return render_to_string(self.get_template, {
            'widget': self,
            'request': options['request'],
            'page': page,
            'title': title,
            'subtitle': subtitle,
        })
