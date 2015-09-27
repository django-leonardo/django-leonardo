# -#- coding: utf-8 -#-

from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from leonardo.module.nav.forms import NavigationForm
from leonardo.module.nav.models import NavigationWidget


class ContentNavigationWidget(NavigationWidget):
    include_contextual_pages = models.BooleanField(
        verbose_name=_("Display included pages"), default=False)
    include_text_headers = models.BooleanField(
        verbose_name=_("Display widget headers"), default=False)

    class Meta:
        abstract = True
        verbose_name = _("Content navigation")
        verbose_name_plural = _('Content navigations')

    feincms_item_editor_form = NavigationForm

    def render_content(self, options):
        request = options['request']
        page = request.webcms_page

        region = 'col3'
        headers = []
        contents = page.content.col3
        """
        for content in contents:
            if content.options.get('label', False):
                headers.append(content)
        """

        return render_to_string(self.get_template_name(), {
            'widget': self,
            'request': options['request'],
            'headers': headers,
            'page': page,
        })
