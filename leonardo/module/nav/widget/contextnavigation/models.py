# -#- coding: utf-8 -#-

from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from leonardo.module.web.const import PAGE_REGIONS
from leonardo.module.web.models import Page, Widget
from leonardo.utils.memoized import memoized


DEPTH_CHOICES = (
    (0, _("self")),
    (1, _("one level")),
    (2, _("all levels")),
)

LINK_CHOICES = (
    ('', _("none")),
    ('link', _("link")),
    ('button', _("button")),
)


class ContextNavigationWidget(Widget):
    root = models.ForeignKey(Page, blank=True, null=True, verbose_name=_("source"), related_name="context_root", help_text=_('The child pages of root page are displayed in the context navigation.'))
    page_region = models.CharField(max_length=255, verbose_name=_("display region"), choices=PAGE_REGIONS, default='preview', help_text=_('Which region of selected pages do you wish to display.'))
    depth = models.IntegerField(verbose_name=_("depth"), choices=DEPTH_CHOICES, default=1, help_text=_('Depth to which display child pages.'))
    link_style = models.CharField(max_length=255, verbose_name=_("link style"), choices=LINK_CHOICES, default='link', blank=True, help_text=_('Visual style of links to displayed pages.'))
    link_text = models.CharField(max_length=255, verbose_name=_("link texts"), default='', blank=True, help_text=_('Arbitrary text of links. If empty, page\'s title will be used instead.'))

    class Meta:
        abstract = True
        verbose_name = _("Contextual content")
        verbose_name_plural = _('Contextual contents')

    @memoized
    def render_content(self, options):

        if self.root:
            root = self.root
        else:
            root = options['request'].webcms_page

        return render_to_string(self.get_template_name(), { 
            'widget': self,
            'page': root,
            'request': options['request'],
            'region': self.page_region,
        })
