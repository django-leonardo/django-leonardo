# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from hrcms.models import Widget

from hrcms.module.links.models import LinkCategory, Link


class LinkMenuWidget(Widget):
    list = models.ForeignKey(LinkCategory, verbose_name=_("link category"))

    def get_links(self):
        return Link.objects.filter(category=self.list, visible=True).order_by('ordering')

    class Meta:
        abstract = True
        verbose_name = _("links menu")
        verbose_name_plural = _('links menus')
