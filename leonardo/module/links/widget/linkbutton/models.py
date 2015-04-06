# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from hrcms.models import Widget
from hrcms.module.links.models import Link

SIZE_CHOICES = (
    ('normal', _('normal')),
    ('large', _('large')),
)

PRIORITY_CHOICES = (
    ('primary', _('primary')),
    ('secondary', _('secondary')),
)

ALIGN_CHOICES = (
    ('left', _('left')),
    ('right', _('right')),
)

ON_CLICK_CHOICES = (
    ('go_to_page', _('go to linked page')),
    ('open_modal', _('open in modal window')),
    ('open_tab', _('open in new window/tab')),
)

class LinkButtonWidget(Widget):
    link = models.ForeignKey(Link, verbose_name=_("link"), blank=True, null=True)
    alt_link = models.CharField(max_length=255, verbose_name=_("alt. link"), blank=True, help_text=_("You can use relative or absolute URLs."))
    text = models.CharField(max_length=255, verbose_name=_("text"), blank=True)
    size = models.CharField(max_length=255, verbose_name=_("size"), choices=SIZE_CHOICES, default="normal")
    priority = models.CharField(max_length=255, verbose_name=_("priority"), choices=PRIORITY_CHOICES, default="primary")
    alignment = models.CharField(max_length=255, verbose_name=_("alignment"), choices=ALIGN_CHOICES, default='left')
    on_click = models.CharField(max_length=255, verbose_name=_("on click action"), choices=ON_CLICK_CHOICES, default='go_to_page')

    class Meta:
        abstract = True
        verbose_name = _("link button")
        verbose_name_plural = _('link buttons')
