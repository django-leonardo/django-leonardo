# -#- coding: utf-8 -#-

from django.utils.translation import ugettext_lazy as _
from form_designer.models import FormContent
from leonardo.module.web.models import Widget


class FormWidget(FormContent, Widget):

    class Meta:
        abstract = True
        verbose_name = _('form')
        verbose_name_plural = _('forms')

    template = 'widget/form/default.html'
