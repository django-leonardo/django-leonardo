
from django.db.models.fields import BLANK_CHOICE_DASH
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import Layout, Fieldset
from django.http import HttpResponseRedirect
from leonardo import forms
from django.utils.translation import ugettext_lazy as _
from leonardo.forms import SelfHandlingForm
from leonardo.module.web.models import Page, PageTheme, PageColorScheme
from leonardo.module.web.const import PAGE_LAYOUT_CHOICES
from leonardo.module.web.page.forms import PageColorSchemeSwitchableFormMixin
from django_select2.forms import Select2Widget


class PageMassChangeForm(SelfHandlingForm, PageColorSchemeSwitchableFormMixin):

    """Page Mass Update

    Form for mass update of page theme, color scheme and layout

    """

    page_id = forms.IntegerField(
        label=_('Page ID'), widget=forms.widgets.HiddenInput)

    theme = forms.ModelChoiceField(
        label=_('Theme'),
        required=False,
        queryset=PageTheme.objects.all(),
        widget=Select2Widget
    )

    layout = forms.ChoiceField(
        label=_('Layout'),
        choices=BLANK_CHOICE_DASH + list(PAGE_LAYOUT_CHOICES),
        required=False)

    depth = forms.IntegerField(label=_('Depth'), initial=1)
    from_root = forms.BooleanField(label=_('From Root ?'), initial=True)

    def __init__(self, *args, **kwargs):
        super(PageMassChangeForm, self).__init__(*args, **kwargs)

        color_scheme_fields = self.init_color_scheme_switch(
            color_scheme=kwargs['initial'].get('color_scheme', None),
            field_kwargs={'widget': Select2Widget})

        self.helper.layout = Layout(
            TabHolder(
                Tab(_('Options'),
                    'depth',
                    'page_id',
                    'from_root',
                    ),
                Tab(_('Styles'),
                    'layout',
                    Fieldset(
                        'Themes', 'theme', *color_scheme_fields),
                    ),
            ),
        )

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

    def clean(self):
        cleaned = super(PageMassChangeForm, self).clean()
        theme = cleaned['theme']
        cleaned['color_scheme'] = self.cleaned_data['theme__%s' % theme.id]
        return cleaned
