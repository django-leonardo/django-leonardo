# -*- coding: UTF-8 -*-

from django import forms
from django.utils.translation import ugettext as _

class WhoisForm(forms.Form):
    domain = forms.CharField(label=_('domain name'))
