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

def get_page_url(page):
    if page.redirect_to:
        return page.redirect_to
    elif page.template_key == 'layout_void':
        try:
            url = page.active_children()[0].get_navigation_url()
        except:
            url = '.'
        return url
    else:
        return page.get_absolute_url()

class BreadcrumbsWidget(Widget):
    orientation = models.CharField(max_length=255, verbose_name=_("orientation"), choices=ORIENTATION_CHOICES, default="horizontal")
    root_label = models.CharField(max_length=255, verbose_name=_("root label"), blank=True, null=True)

    class Meta:
        abstract = True
        verbose_name = _("breadcrumbs")
        verbose_name_plural = _('breadcrumbs')

    def render_content(self, options):
        request = options['request']
        page = request.webcms_page
        include_self = False
        extension = ''

        try:
            fragments = request._feincms_fragments
        except:
            fragments = {}

        if fragments.has_key("_page_breadcrumbs"):
            extension = fragments["_page_breadcrumbs"].strip()
            if extension == '':
                include_self = True
        else:
            include_self = True

        ancs = page.get_ancestors()
        bc = []
        for anc in ancs:
            if anc.is_root_node():
                bc.append((get_page_url(anc.get_children()[0]), anc.in_navigation, anc.short_title()))
            else:
                bc.append((get_page_url(anc), anc.in_navigation, anc.short_title()))

        if include_self:
            bc.append(('', True, page.short_title()))

        return render_to_string(self.template_name, { 
            'widget': self,
            'page': page,
            "trail": bc,
            "extension": extension,
            "include_self": include_self,
            'request': options['request'],
        })
