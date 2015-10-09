
from __future__ import unicode_literals

from .multiple import MultiSelectField

from django_select2.forms import *


class InitMixin(object):

    '''Support for declaring Model Select Field'''

    def __init__(self, *args, **kwargs):
        super(FileField, self).__init__(
            self.queryset, self.empty_label, *args, **kwargs)


class Select2Field(ModelSelect2Widget, InitMixin):

    pass


class Select2MultipleField(ModelSelect2MultipleWidget, InitMixin):

    pass
