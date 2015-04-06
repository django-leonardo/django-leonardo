# -#- coding: utf-8 -#-

from django import forms
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from hrcms.module.web.models import Widget
from markupfield.fields import MarkupField


class MarkupTextWidget(Widget):
    text = MarkupField(_('text'), blank=True, default=_(
        'Empty text'), default_markup_type='restructuredtext')

    class Meta:
        abstract = True
        verbose_name = _('markup text')
        verbose_name_plural = _('markup texts')

    def save(self, *args, **kwargs):
        if self.text == '' or self.text == None:
            self.text = _('Empty text')
        super(MarkupTextWidget, self).save(*args, **kwargs)
