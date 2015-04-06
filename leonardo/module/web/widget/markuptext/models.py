# -#- coding: utf-8 -#-

from django.forms import widgets
from django.utils.translation import ugettext_lazy as _
from leonardo.module.web.models import Widget
from markitup.fields import MarkupField

# register MarkupField to use the custom widget in the Admin
from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS
FORMFIELD_FOR_DBFIELD_DEFAULTS[MarkupField] = {'widget': widgets.Textarea}


class MarkupTextWidget(Widget):
    text = MarkupField(_('text'), blank=True, default=_(
        'Empty text'))

    class Meta:
        abstract = True
        verbose_name = _('markup text')
        verbose_name_plural = _('markup texts')
