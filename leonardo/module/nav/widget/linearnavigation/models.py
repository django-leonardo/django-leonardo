# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from leonardo.module.web.models import Widget, Page

TRAVERSE_CHOICES = (
    (0, _("none")),
    (1, _("parents")),
    (2, _("siblings")),
    (3, _("cousins")),
)

LINK_CHOICES = (
    ('text', _("previous/next")),
    ('page', _("page title")),
)

class LinearNavigationWidget(Widget):
    traverse = models.IntegerField(verbose_name=_("traverse"), choices=TRAVERSE_CHOICES, default=0)
    link = models.CharField(max_length=255, verbose_name=_("links"), choices=LINK_CHOICES, default='text')

    class Meta:
        abstract = True
        verbose_name = _("linear navigation")
        verbose_name_plural = _('linear navigations')

    def render_content(self, options):
        request = options['request']
        page = request.webcms_page
    
        if self.traverse == 0:
            prev = page.get_previous_sibling()
            next = page.get_next_sibling()
        elif self.traverse == 1:
            prev = page.get_previous_sibling()
            if prev == None:
                prev = page
            next = page.get_next_sibling()
        else:
            prev = page.get_previous_sibling()
            next = page.get_next_sibling()
        return render_to_string(self.get_template_name(), { 
            'widget': self,
            'request': request,
            'prev': prev,
            'next': next,
        })
