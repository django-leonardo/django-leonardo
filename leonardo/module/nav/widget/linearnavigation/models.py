# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from leonardo.module.nav.models import NavigationWidget


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


class LinearNavigationWidget(NavigationWidget):
    traverse = models.IntegerField(
        verbose_name=_("Node traversal"), choices=TRAVERSE_CHOICES, default=0)
    link_style = models.CharField(
        max_length=255, verbose_name=_("Link style"), choices=LINK_CHOICES, default='text')

    class Meta:
        abstract = True
        verbose_name = _("Linear pager")
        verbose_name_plural = _('Linear pagers')

    def render_content(self, options):
        request = options['request']
        page = request.webcms_page

        if self.traverse == 0:
            prev = page.get_previous_sibling()
            next = page.get_next_sibling()
        elif self.traverse == 1:
            prev = page.get_previous_sibling()
            if prev is None:
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
