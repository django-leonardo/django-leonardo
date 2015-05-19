
import copy

import floppyforms as forms
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import Field, HTML, Layout
from django.forms.models import modelform_factory
from django.utils.translation import ugettext_lazy as _
from horizon.utils.memoized import memoized
from horizon_contrib.common import get_class
from leonardo.forms import SelfHandlingModelForm, SelfHandlingForm
from django.utils.text import slugify
from ..models import Page


class PageCreateForm(SelfHandlingModelForm):

    slug = forms.SlugField(required=False, initial=None)

    class Meta:
        model = Page
        widgets = {
            'site': forms.widgets.HiddenInput,
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

        HIDDEN_FIELDS = (
            'site',
        )
        self.fields['parent'].initial = parent
        self.helper.layout = Layout(
            TabHolder(
                Tab(_('Main'),
                    'title',
                    'language',
                    'translation_of',
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
                    'template_key', 'layout', 'theme', 'color_scheme',
                    css_id='page-theme-settings'
                    ),
            )
        )
        # append hidden fields
        [self.helper.layout.append(Field(f)) for f in HIDDEN_FIELDS]

        self._wrap_all()


class PageUpdateForm(SelfHandlingModelForm):

    class Meta:
        model = Page
        widgets = {
            'site': forms.widgets.HiddenInput,
            'parent': forms.widgets.HiddenInput,
            'override_url': forms.widgets.HiddenInput,
        }
        exclude = tuple()

    def _wrap_all(self):
        # stylung
        self.helper.filter(
            basestring, max_level=4).wrap(
            Field, css_class="form-control")

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(PageUpdateForm, self).__init__(*args, **kwargs)

        HIDDEN_FIELDS = (
            'site',
        )

        self.helper.layout = Layout(
            TabHolder(
                Tab(_('Main'),
                    'title',
                    'language',
                    'translation_of',
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
                    'template_key', 'layout', 'theme', 'color_scheme',
                    css_id='page-theme-settings'
                    ),
            )
        )
        # append hidden fields
        [self.helper.layout.append(Field(f)) for f in HIDDEN_FIELDS]

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

        self._wrap_all()


class PageDeleteForm(SelfHandlingForm):

    def handle(self, request, data):
        pass
