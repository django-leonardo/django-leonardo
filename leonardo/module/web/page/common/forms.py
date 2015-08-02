
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import Layout
from django.http import HttpResponseRedirect
from leonardo import forms
from django.utils.translation import ugettext_lazy as _, ugettext
from leonardo.forms import SelfHandlingForm
from leonardo.module.web.fields.page import (AutoHeavySelect2Widget,
                                             PageColorSchemeSelectField,
                                             PageThemeSelectField)
from leonardo.module.web.models import Page
from leonardo.module.web.const import PAGE_LAYOUT_CHOICES


class PageMassChangeForm(SelfHandlingForm):

    """Page Mass Update

    Form for mass update of page theme, color scheme and layout

    """

    page_id = forms.IntegerField(
        label=_('Page ID'), widget=forms.widgets.HiddenInput)

    color_scheme = PageColorSchemeSelectField(
        label=_('Color Scheme'),
        widget=AutoHeavySelect2Widget(
            select2_options={
                'minimumInputLength': 0,
                'placeholder': ugettext('Click to expand.'),
            },
        ),
        required=False
    )

    theme = PageThemeSelectField(
        label=_('Theme'),
        widget=AutoHeavySelect2Widget(
            select2_options={
                'minimumInputLength': 0,
                'placeholder': ugettext('Click to expand.'),
            },
        ),
        required=False
    )

    layout = forms.ChoiceField(
        label=_('Layout'), choices=PAGE_LAYOUT_CHOICES,
        required=False)

    depth = forms.IntegerField(label=_('Depth'), initial=1)
    from_root = forms.BooleanField(label=_('From Root ?'), initial=True)

    def __init__(self, *args, **kwargs):
        super(PageMassChangeForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            TabHolder(
                Tab(_('Options'),
                    'depth',
                    'page_id',
                    'from_root',
                    ),
                Tab(_('Styles'),
                    'layout',
                    'theme',
                    'color_scheme',
                    ),
            ),
        )

        self.fields['layout'].choices.insert(0, ('', _('Select Layout')))

    def handle(self, request, data):

        root_page = Page.objects.get(pk=data['page_id'])

        if data['from_root']:
            root_page = root_page.get_root()

        color_scheme = data.get('color_scheme', None)
        theme = data.get('theme', None)
        layout = data.get('layout', None)

        if color_scheme:
            root_page.color_scheme = data['color_scheme']
        if layout:
            root_page.layout = data['layout']
        if theme:
            root_page.theme = data['theme']

        for page in root_page.get_descendants():

            if page.level <= data['depth']:
                if color_scheme:
                    page.color_scheme = data['color_scheme']
                if layout:
                    page.layout = data['layout']
                if theme:
                    page.theme = data['theme']

                page.save()

        root_page.save()

        return HttpResponseRedirect(root_page.get_absolute_url())
