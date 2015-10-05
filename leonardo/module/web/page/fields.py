
from django import forms
from django_select2.forms import *

from ..models import Page, PageColorScheme, PageTheme
from .widgets import (PageColorSchemeSelectWidget, PageSelectWidget,
                      PageThemeSelectWidget)


class Field(forms.ModelChoiceField):

    def __init__(self, *args, **kwargs):
        super(Field, self).__init__(
            queryset=getattr(self, 'model', Page).objects.all(),
            empty_label='---', *args, **kwargs)

    def label_from_instance(self, obj):
        """
        Coerces ``value`` to a Python data type.
        """
        return obj.tree_label


class PageSelectField(Field):
    '''Page Select2 Field'''
    model = Page
    widget = PageSelectWidget


class PageColorSchemeSelectField(Field):
    '''PageColorScheme Select2 Field'''
    model = PageColorScheme
    widget = PageColorSchemeSelectWidget


class PageThemeSelectField(Field):
    '''PageTheme Select2 Field'''
    model = PageTheme
    widget = PageThemeSelectWidget
