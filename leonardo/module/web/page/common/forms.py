
from django.db.models.fields import BLANK_CHOICE_DASH
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import Layout, Fieldset
from django.http import HttpResponseRedirect
from leonardo import forms
from django.utils.translation import ugettext_lazy as _
from leonardo.forms import SelfHandlingForm
from leonardo.module.web.models import Page
from leonardo.module.web.const import PAGE_LAYOUT_CHOICES
from leonardo.module.web.page.forms import PageColorSchemeSwitchableFormMixin
from leonardo.forms import LanguageSelectField, Select2Widget
from leonardo.module.web.page.fields import PageThemeSelectField
from leonardo.forms.fields.sites import SiteSelectField


class PageMassChangeForm(SelfHandlingForm, PageColorSchemeSwitchableFormMixin):

    """Page Mass Update

    Form for mass update of page theme, color scheme, layout and language

    """

    page_id = forms.IntegerField(
        label=_('Page ID'), widget=forms.widgets.HiddenInput)

    language = LanguageSelectField(
        required=False
    )

    theme = PageThemeSelectField(
        label=_('Theme'),
        required=False
    )

    layout = forms.ChoiceField(
        label=_('Layout'),
        choices=BLANK_CHOICE_DASH + list(PAGE_LAYOUT_CHOICES),
        required=False)

    site = SiteSelectField(
        required=False
    )

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
                    'site',
                    'language',
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
        site = data.get('site', None)
        language = data.get('language', None)

        if color_scheme:
            root_page.color_scheme = color_scheme
        if layout:
            root_page.layout = layout
        if theme:
            root_page.theme = theme
        if site:
            root_page.site = site
        if language:
            root_page.site = language

        for page in root_page.get_descendants():

            if page.level <= data['depth']:
                if language:
                    page.language = language
                if color_scheme:
                    page.color_scheme = color_scheme
                if layout:
                    page.layout = layout
                if theme:
                    page.theme = theme
                if site:
                    page.site = site

                page.save()

        root_page.save()

        return HttpResponseRedirect(root_page.get_absolute_url())

    def clean(self):
        cleaned = super(PageMassChangeForm, self).clean()
        theme = cleaned['theme']

        if theme:
            cleaned['color_scheme'] = self.cleaned_data['theme__%s' % theme.id]

        return cleaned
