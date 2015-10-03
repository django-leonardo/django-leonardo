
from django import forms
from django_select2.forms import *

from ..models import Page, PageColorScheme, PageTheme
from .widgets import (PageColorSchemeSelectWidget, PageSelectWidget,
                      PageThemeSelectWidget)


class Field(forms.ModelChoiceField):
    empty_values = [u'']
    empty_label = "(nothing)"

    def __init__(self, *args, **kwargs):
        super(Field, self).__init__(
            self.queryset, self.empty_label, *args, **kwargs)


class PageSelectField(Field):
    queryset = Page.objects
    widget = PageSelectWidget


class PageColorSchemeSelectField(Field):
    queryset = PageColorScheme.objects
    widget = PageColorSchemeSelectWidget


class PageThemeSelectField(Field):
    queryset = PageTheme.objects
    widget = PageThemeSelectWidget
