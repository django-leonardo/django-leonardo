# -#- coding: utf-8 -#-

from django.utils.translation import ugettext_lazy as _
from leonardo.module.web.models import Widget
from markupfield.fields import MarkupField


class MarkupTextWidget(Widget):
    text = MarkupField(_('text'), blank=True, default=_(
        'Empty text'), default_markup_type='restructuredtext')

    class Meta:
        abstract = True
        verbose_name = _('markup text')
        verbose_name_plural = _('markup texts')
