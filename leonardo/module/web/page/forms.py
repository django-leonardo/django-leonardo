
import copy

import floppyforms as forms
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import Field, HTML, Layout, Fieldset
from django.forms.models import modelform_factory
from django.utils.translation import ugettext_lazy as _
from horizon.utils.memoized import memoized
from django import forms as django_forms
from horizon_contrib.common import get_class
from leonardo.forms import SelfHandlingModelForm, SelfHandlingForm
from django.utils.text import slugify
from ..models import Page, PageTheme, PageColorScheme


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

    def init_color_scheme_switch(self, color_scheme=None):
        color_scheme_fields = []

        for theme in self.fields['theme'].queryset:

            name = 'theme__%s' % theme.id
            attributes = self.get_switched_form_field_attrs(
                'switchable', '%s' % theme.id, ('Color Scheme'))
            field = django_forms.ModelChoiceField(label=_('Color Scheme'),
                                                  queryset=theme.templates.all(),
                                                  required=False)
            # inital for color scheme
            if color_scheme and theme.templates.filter(id=color_scheme.id).exists():
                field.initial = color_scheme
            elif 'parent' in self.fields and self.fields['parent'].initial:
                field.initial = self.fields['parent'].initial.color_scheme
            elif self.instance and hasattr(self.instance, 'color_scheme'):
                field.initial = self.instance.color_scheme
            else:
                field.initial = theme.templates.first()
            self.fields[name] = field
            color_scheme_fields.append(name)

        # update theme widget attributes
        self.fields['theme'].widget.attrs = self.switchable_field_attrs()
        return color_scheme_fields


class PageCreateForm(PageColorSchemeSwitchableFormMixin, SelfHandlingModelForm):

    slug = forms.SlugField(required=False, initial=None)

    class Meta:
        model = Page
        widgets = {
            'parent': forms.widgets.HiddenInput,
        }
        exclude = tuple()

    def clean_slug(self):
        """slug title if is not provided
        """
        slug = self.cleaned_data.get('slug', None)
        if slug is None or len(slug) == 0:
            slug = slugify(self.cleaned_data['title'])
        return slug

    def __init__(self, *args, **kwargs):
        parent = kwargs.pop('parent', None)
        super(PageCreateForm, self).__init__(*args, **kwargs)

        self.fields['parent'].initial = parent
        color_scheme_fields = self.init_color_scheme_switch(
            color_scheme=kwargs['initial'].get('color_scheme', None))

        self.helper.layout = Layout(
            TabHolder(
                Tab(_('Main'),
                    'title',
                    'language',
                    'translation_of',
                    'site',
                    css_id='page-main'
                    ),
                Tab(_('Navigation'),
                    'in_navigation', 'parent', 'slug', 'override_url', 'redirect_to',
                    'symlinked_page'
                    ),
                Tab(_('Heading'),
                    '_content_title', '_page_title',
                    css_id='page-heading'
                    ),
                Tab(_('Publication'),
                    'active', 'featured', 'publication_date', 'publication_end_date',
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
        theme = cleaned['theme']
        cleaned['color_scheme'] = self.cleaned_data['theme__%s' % theme.id]
        return cleaned


class PageUpdateForm(PageColorSchemeSwitchableFormMixin, SelfHandlingModelForm):

    class Meta:
        model = Page
        widgets = {
            'parent': forms.widgets.HiddenInput,
            'override_url': forms.widgets.HiddenInput,
            'publication_date': forms.widgets.DateInput,
        }
        exclude = tuple()

    def clean(self):
        cleaned = super(PageUpdateForm, self).clean()
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
                    'site',
                    css_id='page-main'
                    ),
                Tab(_('Heading'),
                    '_content_title', '_page_title',
                    css_id='page-heading'
                    ),
                Tab(_('Publication'),
                    'active', 'featured', 'publication_date', 'publication_end_date',
                    ),
                Tab(_('Navigation'),
                    'in_navigation', 'parent', 'slug', 'override_url', 'redirect_to',
                    'symlinked_page'
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
                _request, page=page, data=page.dimensions, needs_form_wrapper=False)
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
