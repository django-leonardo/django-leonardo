# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from feincms.module.page.models import Page

from hrcms.models import Widget

ORIENTATION_CHOICES = (
    ('horizontal', _("horizontal")),
    ('vertical', _("vertical")),
)

PRIORITY_CHOICES = (
    ('primary', _("primary")),
    ('secondary', _("secondary")),
    ('common', _("common")),
)

DEPTH_CHOICES = (
    (1, _("only one level")),
    (2, _("subpages too")),
)

class TreeNavigationWidget(Widget):
    orientation = models.CharField(max_length=255, verbose_name=_("orientation"), choices=ORIENTATION_CHOICES, default="horizontal")
    priority = models.CharField(max_length=255, verbose_name=_("priority"), choices=PRIORITY_CHOICES, default="primary")
    depth = models.IntegerField(verbose_name=_("depth"), choices=DEPTH_CHOICES, default=1)
    root = models.ForeignKey(Page, blank=True, null=True, verbose_name=_("root page"), related_name="taxonomy_root", help_text=_("If no root page is set, widget's parent page will be used."))

    class Meta:
        abstract = True
        verbose_name = _("navigation menu")
        verbose_name_plural = _('navigation menus')

    def level(self, level):
        return level + 2

    def render_content(self, options):
        request = options['request']

        if self.root:
            root = self.root
        else:
            root = self.parent

        return render_to_string(self.template_name, { 
            'widget': self,
            'current': request.webcms_page,
            'root': root,
            'lvl': self.level(root.level),
            'lvl2': self.level(root.level+1),
            'lvl3': self.level(root.level+2),
            'lvl4': self.level(root.level+3),
            'lvl5': self.level(root.level+4),
            'lvl6': self.level(root.level+5),
            'depth': self.depth,
            'request': options['request'],
        })
