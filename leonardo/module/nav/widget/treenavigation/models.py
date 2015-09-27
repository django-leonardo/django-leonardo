# -#- coding: utf-8 -#-

from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from leonardo.module.nav.forms import NavigationForm
from leonardo.module.nav.models import NavigationWidget
from leonardo.module.web.models import Page

DEPTH_CHOICES = (
    (1, _("Only one level")),
    (2, _("Include subpages")),
)
LINK_CHOICES = (
    ('default', _('Default title')),
    ('detail', _('Detailed title')),
)


class TreeNavigationWidget(NavigationWidget):
    depth = models.IntegerField(verbose_name=_("depth"), choices=DEPTH_CHOICES, default=1)
    root = models.ForeignKey(Page, blank=True, null=True, verbose_name=_(
        "root page"), related_name="taxonomy_root", help_text=_("If not set, widget's parent page will be used as root page."))
    link_style = models.CharField(
        max_length=255, verbose_name=_("Link style"), choices=LINK_CHOICES, default='default')

    class Meta:
        abstract = True
        verbose_name = _("Navigation menu")
        verbose_name_plural = _('Navigation menus')

    feincms_item_editor_form = NavigationForm

    def level(self, level):
        return level + 2

    def render_content(self, options):
        request = options['request']

        if self.root:
            root = self.root
        else:
            root = self.parent

        return render_to_string(self.get_template_name(), {
            'widget': self,
            'current': getattr(request, 'leonardo_page', None),
            'root': root,
            'level': self.level(root.level),
            'level2': self.level(root.level) + 1,
            'depth': self.depth,
            'request': request,
        })
