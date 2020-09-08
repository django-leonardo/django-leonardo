
from __future__ import unicode_literals

from django.conf import settings
from django.forms import ChoiceField
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import *

from .multiple import MultiSelectField


class InitMixin(object):

    '''Support for declaring Model Select Field'''

    def __init__(self, *args, **kwargs):
        super(FileField, self).__init__(
            self.queryset, self.empty_label, *args, **kwargs)


class Select2Field(ModelSelect2Widget, InitMixin):

    pass


class Select2MultipleField(ModelSelect2MultipleWidget, InitMixin):

    pass


class LanguageSelectField(ChoiceField):

    def __init__(self, *args, **kwargs):
        super(LanguageSelectField, self).__init__(
            label=_("Language"),
            choices=settings.LANGUAGES,
            widget=Select2Widget,
            *args, **kwargs)
