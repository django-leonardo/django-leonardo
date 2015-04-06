# -#- coding: utf-8 -#-

from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.template import RequestContext

from webcms.models import Widget

SCOPE_CHOICES = (
    ('theme', _('theme')),
    ('template', _('template')),
)

class ThemeSwitcherWidget(Widget):
    scope = models.CharField(max_length=255, verbose_name=_("scope"), default="theme", choices=SCOPE_CHOICES)

    class Meta:
        abstract = True
        verbose_name = _("theme switcher")
        verbose_name_plural = _('theme switchers')
