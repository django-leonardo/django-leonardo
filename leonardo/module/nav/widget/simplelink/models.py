# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.utils.translation import get_language_from_request

from leonardo.module.web.models import Widget, Page


class SimpleLinkWidget(Widget):

    page = models.ForeignKey(Page, verbose_name=_(
        "Linked page"), related_name="simplelink_node")

    class Meta:
        abstract = True
        verbose_name = _("Simple link")
        verbose_name_plural = _('Simple links')

    def render_content(self, options):
        request = options['request']

        return render_to_string(self.get_template_name(), {
            'widget': self,
            'request': request,
        })
