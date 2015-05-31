
from django_select2.fields import *

from django_select2.widgets import *


class Field(AutoModelSelect2Field):
    empty_values = [u'']
