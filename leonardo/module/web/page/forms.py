
import copy

import floppyforms as forms
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import HTML, Field, Fieldset, Layout
from django import forms as django_forms
from django.forms.models import modelform_factory
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import Select2Widget
from horizon.utils.memoized import memoized
from horizon_contrib.common import get_class
from leonardo.forms import SelfHandlingForm, SelfHandlingModelForm
from leonardo.forms.fields.sites import SiteSelectField

from ..models import Page, PageColorScheme, PageTheme
from .fields import PageSelectField


class SwitchableFormFieldMixin(object):

    def get_switched_form_field_attrs(self, prefix, input_type, name):
        """Creates attribute dicts for the switchable theme form
        """
        attributes = {'class': 'switched', 'data-switch-on': prefix + 'field'}
        attributes['data-' + prefix + 'field-' + input_type] = name
        return attributes

    def switchable_field_attrs(self):
        return {'class': 'switchable',
                'data-slug': 'switchablefield'
                }


class PageColorSchemeSwitchableFormMixin(SwitchableFormFieldMixin):

    def init_color_scheme_switch(self, color_scheme=None, field_kwargs={}):
        color_scheme_fields = []

        for theme in self.fields['theme'].queryset:

            name = 'theme__%s' % theme.id
            attributes = self.get_switched_form_field_attrs(
                'switchable', '%s' % theme.id, ('Color Scheme'))
            field = django_forms.ModelChoiceField(
                label=_('Color Scheme'),
                queryset=theme.templates.all(),
                required=False,
                **field_kwargs)
            # inital for color scheme
            if color_scheme and theme.templates.filter(
                    id=color_scheme.id).exists():
                field.initial = color_scheme
            elif 'parent' in self.fields and self.fields['parent'].initial:
                field.initial = self.fields['parent'].initial.color_scheme
            elif hasattr(self, 'instance') \
                    and hasattr(self.instance, 'color_scheme'):
                field.initial = self.instance.color_scheme
            else:
                field.initial = theme.templates.first()
            field.widget.attrs = attributes
            self.fields[name] = field
            color_scheme_fields.append(name)

        # update theme widget attributes
        self.fields['theme'].widget.attrs = self.switchable_field_attrs()
        return color_scheme_fields


class PageCreateForm(PageColorSchemeSwitchableFormMixin,
                     SelfHandlingModelForm):

    slug = forms.SlugField(required=False, initial=None)

    parent = PageSelectField(required=False)
    translation_of = PageSelectField(required=False)
    symlinked_page = PageSelectField(required=False)
    site = SiteSelectField()

    class Meta:
        model = Page
        widgets = {
            'parent': forms.widgets.HiddenInput,
            'theme': Select2Widget,
            'language': Select2Widget,
        }
        exclude = tuple()

    def clean_slug(self):
        """slug title if is not provided
        """
        slug = self.cleaned_data.get('slug', None)
        if slug is None or len(slug) == 0 and 'title' in self.cleaned_data:
            slug = slugify(self.cleaned_data['title'])
        return slug

    def __init__(self, request, *args, **kwargs):
        parent = kwargs.pop('parent', None)
        super(PageCreateForm, self).__init__(*args, **kwargs)

        if parent:
            self.fields['parent'].initial = parent

        if request.method == 'GET':
            color_scheme_fields = self.init_color_scheme_switch(
                color_scheme=kwargs['initial'].get('color_scheme', None))

            self.helper.layout = Layout(
                TabHolder(
                    Tab(_('Main'),
                        'title',
                        'language',
                        'translation_of',
                        'parent',
                        'site',
                        css_id='page-main'
                        ),
                    Tab(_('Navigation'),
                        'in_navigation', 'slug',
                        'override_url', 'redirect_to',
                        'symlinked_page', 'navigation_extension'
                        ),
                    Tab(_('Heading'),
                        '_content_title', '_page_title',
                        css_id='page-heading'
                        ),
                    Tab(_('Publication'),
                        'active', 'featured', 'publication_date',
                        'publication_end_date', 'meta_description',
                        'meta_keywords'
                        ),
                    Tab(_('Theme'),
                        'template_key', 'layout', Fieldset(
                            'Themes', 'theme', *color_scheme_fields),
                        css_id='page-theme-settings'
                        ),
                )
            )

        self.fields['color_scheme'].required = False

    def clean(self):
        cleaned = super(PageCreateForm, self).clean()

        if 'theme' in cleaned:

            if cleaned['parent']:
                theme = cleaned['parent'].theme
                cleaned['theme'] = theme
            else:
                theme = cleaned['theme']

            # small combo
            value = self.fields['color_scheme'].widget.value_from_datadict(
                self.data, self.files, self.add_prefix('theme__%s' % theme.id))

            cleaned['color_scheme'] = self.fields['color_scheme'].clean(value)

        return cleaned


class PageUpdateForm(PageColorSchemeSwitchableFormMixin,
                     SelfHandlingModelForm):

    parent = PageSelectField(required=False)
    translation_of = PageSelectField(required=False)
    symlinked_page = PageSelectField(required=False)
    site = SiteSelectField()

    class Meta:
        model = Page
        widgets = {
            'publication_date': forms.widgets.DateInput,
            'language': Select2Widget,
            'navigation_extension': Select2Widget
        }
        exclude = tuple()

    def clean(self):
        cleaned = super(PageUpdateForm, self).clean()

        if 'theme' in cleaned:
            theme = cleaned['theme']
            cleaned['color_scheme'] = self.cleaned_data['theme__%s' % theme.id]

        return cleaned

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(PageUpdateForm, self).__init__(*args, **kwargs)

        color_scheme_fields = self.init_color_scheme_switch()

        self.helper.layout = Layout(
            TabHolder(
                Tab(_('Main'),
                    'title',
                    'language',
                    'translation_of',
                    'parent',
                    'site',
                    css_id='page-main'
                    ),
                Tab(_('Heading'),
                    '_content_title', '_page_title',
                    css_id='page-heading'
                    ),
                Tab(_('Publication'),
                    'active', 'featured', 'publication_date',
                    'publication_end_date', 'meta_description',
                    'meta_keywords'
                    ),
                Tab(_('Navigation'),
                    'in_navigation', 'slug',
                    'override_url', 'redirect_to',
                    'symlinked_page', 'navigation_extension'
                    ),
                Tab(_('Theme'),
                    'template_key', 'layout', Fieldset(
                        'Themes', 'theme', *color_scheme_fields),
                    css_id='page-theme-settings'
                    ),
            )
        )

        if request:
            _request = copy.copy(request)
            _request.POST = {}

            if kwargs.get('instance', None):
                page = kwargs['instance']

                from .tables import PageDimensionTable
                table = PageDimensionTable(
                    _request, page=page, data=page.dimensions,
                    needs_form_wrapper=False)
                dimensions = Tab(_('Dimensions'),
                                 HTML(
                    table.render()),
                    css_id='page-dimensions'

                )
                self.helper.layout[0].append(dimensions)

        self.fields['color_scheme'].required = False


class PageDeleteForm(SelfHandlingForm):

    def handle(self, request, data):
        pass
