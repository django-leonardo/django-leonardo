
from django_select2.forms import ModelSelect2Widget
from leonardo.models import Page, PageColorScheme, PageTheme


class PageSelectWidget(ModelSelect2Widget):

    model = Page

    search_fields = ['title__icontains', ]

    def label_from_instance(self, obj):
        """
        Coerces ``value`` to a Python data type.
        """
        return obj.tree_label


class PageColorSchemeSelectWidget(ModelSelect2Widget):

    model = PageColorScheme

    search_fields = ['label__icontains', 'name__icontains']


class PageThemeSelectWidget(ModelSelect2Widget):

    model = PageTheme

    search_fields = ['label__icontains', 'name__icontains']
