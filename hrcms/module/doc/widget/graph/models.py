# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from webcms.models import Widget

from webcms.module.media.models import File 

VIEWPORT_CHOICES = (
    ('full', _('Full')),
)

class GraphWidget(Widget):
    file = models.ForeignKey(File, verbose_name=_("graph"), limit_choices_to={'type': 'graph'})
    width = models.CharField(max_length=25, verbose_name=_("width"), default='100%')
    height = models.CharField(max_length=25, verbose_name=_("height"), default='600')
    toolbar = models.BooleanField(verbose_name=_("toolbar"), default=False)
    overview = models.BooleanField(verbose_name=_("overview"), default=False)
    movable = models.BooleanField(verbose_name=_("movable"), default=False)
    tooltips = models.BooleanField(verbose_name=_("tooltips"), default=True)
    links = models.BooleanField(verbose_name=_("links"), default=True)
    links_in_new_window = models.BooleanField(verbose_name=_("open in new window"), default=False)
    viewport = models.CharField(max_length=255, verbose_name=_("viewport"), choices=VIEWPORT_CHOICES, default='full')

    class Meta:
        abstract = True
        verbose_name = _("simple graph")
        verbose_name_plural = _('simple graphs')
