
from __future__ import unicode_literals

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
