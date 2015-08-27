# -#- coding: utf-8 -#-

from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from leonardo.module.nav.models import NavigationWidget


def get_page_url(page):
    if page.redirect_to:
        return page.redirect_to
    else:
        return page.get_absolute_url()

class BreadcrumbsWidget(NavigationWidget):
    root_text = models.CharField(
        max_length=255, verbose_name=_("Root node label"), blank=True, null=True)

    class Meta:
        abstract = True
        verbose_name = _("Breadcrumb trail")
        verbose_name_plural = _('Breadcrumb trails')

    def render_content(self, options):
        request = options['request']
        page = request.leonardo_page
        include_self = False
        extension = ''

        try:
            fragments = request._feincms_fragments
        except:
            fragments = {}

        if '_breadcrumbs' in fragments:
            extension = fragments["_breadcrumbs"].strip()
            if extension == '':
                include_self = True
        else:
            include_self = True

        ancs = page.get_ancestors()
        bc = []
        for anc in ancs:
            if anc.is_root_node():
                bc.append(
                    (get_page_url(anc.get_children()[0]), anc.in_navigation, anc.short_title()))
            else:
                bc.append((get_page_url(anc), anc.in_navigation, anc.short_title()))

        if include_self:
            bc.append(('', True, page.short_title()))

        return render_to_string(self.get_template_name(), {
            'widget': self,
            'page': page,
            "trail": bc,
            "extension": extension,
            "include_self": include_self,
            'request': options['request'],
        })
