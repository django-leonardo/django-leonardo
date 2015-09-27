
from __future__ import unicode_literals

from .multiple import MultiSelectField

from django_select2.fields import AutoModelSelect2Field

from django_select2 import AutoModelSelect2MultipleField
from django_select2.widgets import *


class Select2Field(AutoModelSelect2Field):
    empty_values = [u'']


class Select2MultipleField(AutoModelSelect2MultipleField):
    empty_values = [u'']


class SimpleSelect2Widget(AutoHeavySelect2Widget):

    def __init__(self, **kwargs):

        super(SimpleSelect2Widget, self).__init__(**kwargs)

        self.options['minimumInputLength'] = 0
        self.options['placeholder'] = 'Click to expand.'
