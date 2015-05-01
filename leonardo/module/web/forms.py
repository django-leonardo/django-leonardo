
import copy
from crispy_forms.bootstrap import Tab, TabHolder, Accordion, AccordionGroup
from crispy_forms.layout import Field, HTML, Layout
from django import forms
from django.contrib.auth import get_permission_codename
from django.db.models.loading import get_model
from django.forms.models import modelform_factory
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from feincms.admin.item_editor import ItemEditorForm
from horizon.utils.memoized import memoized
from horizon_contrib.common import get_class
from horizon_contrib.forms import SelfHandlingForm, SelfHandlingModelForm
from redactor.widgets import RedactorEditor

WIDGETS = {
    'template_name': forms.RadioSelect(choices=[]),
    'parent': forms.widgets.HiddenInput,
    'ordering': forms.widgets.HiddenInput,
    'text': RedactorEditor(),
}


class WidgetUpdateForm(ItemEditorForm, SelfHandlingModelForm):

    id = forms.CharField(
        widget=forms.widgets.HiddenInput,
        required=False
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(WidgetUpdateForm, self).__init__(*args, **kwargs)

        queryset = self.fields['content_theme'].queryset

        self.fields['content_theme'].queryset = \
            queryset.filter(widget_class=self._meta.model.__name__)
        from .tables import WidgetDimensionTable
        self.helper.layout = Layout(
            TabHolder(
                Tab(self._meta.model._meta.verbose_name.capitalize(),
                    *self._meta.model.fields(),
                    css_id='field-{}'.format(slugify(self._meta.model))
                    ),
                Tab(_('Theme'),
                    'base_theme', 'content_theme', 'label', 'id',
                    'region', 'ordering', 'parent',
                    ),
            )
        )
        # append preview tab if is ready
        if 'initial' in kwargs \
                and kwargs['initial'].get('prerendered_content', None):

            preview = Tab(_('Preview'),
                          HTML(kwargs['initial'].get('prerendered_content')),
                          )

            self.helper.layout[0].append(preview)

        self.fields['label'].widget = \
            forms.TextInput(
                attrs={'placeholder': self._meta.model._meta.verbose_name})

        if request:
            _request = copy.copy(request)
            _request.POST = {}
            initial = kwargs.get('initial', None)
            if initial and initial.get('id', None):
                widget = self._meta.model.objects.get(
                    id=initial['id'])
                data = widget.dimensions
            else:
                data = []
                widget = None
            dimensions = Tab(_('Dimensions'),
                             HTML(
                                 WidgetDimensionTable(_request, widget=widget, data=data).render()),
                             )
            self.helper.layout[0].append(dimensions)

        # hide label
        if 'text' in self.fields:
            self.fields['text'].label = ''


class WidgetCreateForm(WidgetUpdateForm):

    class Meta:
        exclude = ['id']

    def __init__(self, *args, **kwargs):
        super(WidgetCreateForm, self).__init__(*args, **kwargs)

        queryset = self.fields['content_theme'].queryset

        self.fields['content_theme'].queryset = \
            queryset.filter(widget_class=self._meta.model.__name__)

        self.fields['content_theme'].initial = \
            self.fields['content_theme'].queryset.first()

        self.fields['base_theme'].initial = \
            self.fields['base_theme'].queryset.first()


class WidgetDeleteForm(SelfHandlingForm):

    def handle(self, request, data):
        pass


class WidgetSelectForm(SelfHandlingForm):

    cls_name = forms.ChoiceField(
        label="Widget Type",
        choices=[],
        required=True
    )

    page_id = forms.IntegerField(
        widget=forms.widgets.HiddenInput,
    )

    ordering = forms.IntegerField(
        widget=forms.widgets.HiddenInput,
        initial=0
    )
    region = forms.CharField(
        widget=forms.widgets.HiddenInput,
    )
    parent = forms.IntegerField(
        widget=forms.widgets.HiddenInput,
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        page_id = kwargs.pop('page_id', None)
        region_name = kwargs.pop('region', None)
        self.next_view = kwargs.pop('next_view', None)

        Page = get_model('web', 'Page')
        page = Page.objects.get(id=page_id)

        super(WidgetSelectForm, self).__init__(*args, **kwargs)

        self.fields['page_id'].initial = page.id
        self.fields['region'].initial = region_name
        self.fields['parent'].initial = page.id

        grouped = {}
        ungrouped = []
        choices = []

        if request.user:
            for ct in page._feincms_content_types:
                # Skip cts that we shouldn't be adding anyway
                opts = ct._meta
                perm = opts.app_label + "." + \
                    get_permission_codename('add', opts)
                if not request.user.has_perm(perm):
                    continue

                ct_info = (ct.__name__.lower(), ct._meta.verbose_name)
                if hasattr(ct, 'optgroup'):
                    if ct.optgroup in grouped:
                        grouped[ct.optgroup].append(ct_info)
                    else:
                        grouped[ct.optgroup] = [ct_info]
                else:
                    ungrouped.append(ct_info)
                choices.append(ct_info)

        self.fields['cls_name'].choices = choices

        self.helper.layout = Layout(
            Field('region'),
            Field('parent'),
            Field('page_id'),
            Field('ordering'),
            HTML(render_to_string("widget/content_type_selection_widget.html", {'grouped': grouped, 'ungrouped': ungrouped}),
                 ),
        )

    def handle(self, request, data):
        # NOTE (majklk): This is a bit of a hack, essentially rewriting this
        # request so that we can chain it as an input to the next view...
        # but hey, it totally works.
        request.method = 'GET'

        return self.next_view.as_view()(request, **data)


class PageUpdateForm(SelfHandlingModelForm):

    class Meta:
        widgets = {
            'site': forms.widgets.HiddenInput,
            'parent': forms.widgets.HiddenInput,
            'override_url': forms.widgets.HiddenInput,
        }

    def __init__(self, *args, **kwargs):
        super(PageUpdateForm, self).__init__(*args, **kwargs)

        HIDDEN_FIELDS = (
            'site', 'id', 'tree_id',
            'parent', 'override_url',
        )

        self.helper.layout = Layout(
            TabHolder(
                Tab(_('Page'),
                    Accordion(
                        AccordionGroup('',
                                       'title', 'slug', 'in_navigation', 'active'
                                       ),
                        AccordionGroup(_('Translation'),
                                       'language'
                                       ),
                        AccordionGroup(_('Publication'),
                                       'publication_date', 'publication_end_date',
                                       )
                ),
                ),
                Tab(_('Theme'),
                    'template_key', 'theme', 'color_scheme',
                    ),
                Tab(_('Other'),
                    '',
                    ),
            )
        )
        # append hidden fields
        [self.helper.layout.append(Field(f)) for f in HIDDEN_FIELDS]


@memoized
def get_widget_update_form(**kwargs):
    """
    widget = get_widget_from_id(widget_id)

    """
    model_cls = get_class(kwargs['cls_name'])

    form_class_base = getattr(
        model_cls, 'feincms_item_editor_form', WidgetUpdateForm)

    WidgetModelForm = modelform_factory(model_cls,
                                        exclude=[],
                                        form=form_class_base,
                                        widgets=WIDGETS)

    return WidgetModelForm


@memoized
def get_widget_create_form(**kwargs):
    """
    widget = get_widget_from_id(widget_id)

    """
    model_cls = get_class(kwargs['cls_name'])

    form_class_base = getattr(
        model_cls, 'feincms_item_editor_form', WidgetCreateForm)

    WidgetModelForm = modelform_factory(model_cls,
                                        exclude=[],
                                        form=form_class_base,
                                        widgets=WIDGETS)

    return WidgetModelForm


@memoized
def get_page_update_form(**kwargs):

    model_cls = get_class('web.page')

    PageModelForm = modelform_factory(model_cls,
                                      exclude=[],
                                      form=PageUpdateForm)

    return PageModelForm
