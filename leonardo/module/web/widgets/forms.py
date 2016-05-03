
import copy

import floppyforms
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import HTML, Field, Fieldset, Layout
from django import forms
from django.apps import apps
from django.forms.models import modelform_factory
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import Select2Widget
from feincms.admin.item_editor import ItemEditorForm
from horizon_contrib.common import get_class
from leonardo.forms import SelfHandlingForm, SelfHandlingModelForm
from leonardo.utils.widgets import get_grouped_widgets


class IconPreviewSelect(floppyforms.widgets.Select):
    template_name = 'floppyforms/select_preview.html'


WIDGETS = {
    'template_name': forms.RadioSelect(choices=[]),
    'parent': forms.widgets.HiddenInput,
    'ordering': forms.widgets.HiddenInput,
    'icon': IconPreviewSelect(attrs={'style': "font-family: 'FontAwesome', Helvetica;"}),
}


class WidgetForm(ItemEditorForm, SelfHandlingModelForm):

    '''Generic Widget Form

        tabs = {
            'tab1': {
                'name': 'Verbose Name'
                'fields': ('field_name1',)
            }
        }

    '''

    id = forms.CharField(
        widget=forms.widgets.HiddenInput,
        required=False
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(WidgetForm, self).__init__(*args, **kwargs)

        initial = kwargs.get('initial', None)
        if initial and initial.get('id', None):
            widget = self._meta.model.objects.get(
                id=initial['id'])
            data = widget.dimensions

            # filter content themes by widget
            queryset = self.fields['content_theme'].queryset
            self.fields['content_theme'].queryset = \
                queryset.filter(widget_class=self._meta.model.__name__)

        else:
            data = []
            widget = None

            # set defaults and delete id field
            self.init_themes()
            del self.fields['id']

        # get all fields for widget
        main_fields = self._meta.model.fields()
        main_fields.update({'label': 'label'})

        self.helper.layout = Layout(
            TabHolder(
                Tab(self._meta.model._meta.verbose_name.capitalize(),
                    *self.get_main_fields(main_fields),
                    css_id='field-{}'.format(slugify(self._meta.model))
                    ),
                Tab(_('Styles'),
                    'base_theme', 'content_theme', 'color_scheme',
                    Fieldset(_('Positions'), 'layout', 'align',
                             'vertical_align'),
                    'id', 'region', 'ordering',
                    'parent',
                    css_id='theme-widget-settings'
                    ),
                Tab(_('Effects'),
                    'enter_effect_style', 'enter_effect_duration',
                    'enter_effect_delay', 'enter_effect_offset',
                    'enter_effect_iteration',
                    css_id='theme-widget-effects'
                    ),
            )
        )

        self.fields['label'].widget = \
            forms.TextInput(
                attrs={'placeholder': self._meta.model._meta.verbose_name})

        if request:
            _request = copy.copy(request)
            _request.POST = {}
            _request.method = 'GET'
            from .tables import WidgetDimensionTable
            dimensions = Tab(_('Dimensions'),
                             HTML(
                                 WidgetDimensionTable(_request,
                                                      widget=widget,
                                                      data=data).render()),
                             )
            self.helper.layout[0].append(dimensions)

        # hide label
        if 'text' in self.fields:
            self.fields['text'].label = ''

        # finally add custom tabs
        self.init_custom_tabs()

    def init_themes(self):
        queryset = self.fields['content_theme'].queryset

        self.fields['content_theme'].queryset = \
            queryset.filter(widget_class=self._meta.model.__name__)

        try:
            base_theme = self.fields['base_theme'].queryset.get(
                name__icontains='default')
        except:
            self.fields['base_theme'].initial = \
                self.fields['base_theme'].queryset.first()
        else:
            self.fields['base_theme'].initial = base_theme

        try:
            content_theme = self.fields['content_theme'].queryset.get(
                name__icontains='default')
        except:
            self.fields['content_theme'].initial = \
                self.fields['content_theme'].queryset.first()
        else:
            self.fields['content_theme'].initial = content_theme


class WidgetUpdateForm(WidgetForm):

    '''obsolete name'''

    pass


class WidgetCreateForm(WidgetUpdateForm):

    ''''''

    pass


class WidgetDeleteForm(SelfHandlingForm):

    def handle(self, request, data):
        pass


class WidgetSelectForm(SelfHandlingForm):

    cls_name = forms.ChoiceField(
        label="Widget Type",
        choices=[],
        required=True,
        widget=Select2Widget()
    )

    first = forms.BooleanField(
        label=('First'),
        help_text=_('If is checked, widget will be'
                    ' placed as first widget in this region'),
        initial=False,
        required=False
    )

    page_id = forms.IntegerField(
        widget=forms.widgets.HiddenInput,
    )

    ordering = forms.IntegerField(
        widget=forms.widgets.HiddenInput,
        initial=99
    )
    region = forms.ChoiceField(
        label=('Region'),
        widget=Select2Widget()
    )
    parent = forms.IntegerField(
        widget=forms.widgets.HiddenInput,
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        page_id = kwargs.pop('page_id', None)
        region_name = kwargs.pop('region', None)
        feincms_cls_name = kwargs.pop('cls_name', None)
        self.next_view = kwargs.pop('next_view', None)

        module, cls = feincms_cls_name.split('.')
        ObjectCls = apps.get_model(module, cls)
        feincms_object = ObjectCls.objects.get(id=page_id)

        super(WidgetSelectForm, self).__init__(*args, **kwargs)

        self.fields['page_id'].initial = feincms_object.id
        self.fields['region'].initial = region_name

        # load template regions
        self.fields['region'].choices = \
            [(str(region.key),
              '%s%s' % (
                str(region.title),
                ' - Inherited' if region.inherited else ''))
             for region in feincms_object.template.regions]

        if region_name:
            self.fields['ordering'].initial = \
                len(getattr(feincms_object.content, region_name, [])) + 1

        self.fields['parent'].initial = feincms_object.id

        choices, grouped, ungrouped = get_grouped_widgets(
            feincms_object, request)

        # reduce choices for validation
        self.fields['cls_name'].choices = [(str(choice[0]), str(choice[1]))
                                           for choice in choices]

        # for now ungrouped to grouped
        grouped['Web'] = ungrouped + grouped.get('Web', [])

        self.helper.layout = Layout(
            Field('parent'),
            Field('page_id'),
            Field('ordering'),
            'cls_name',
            Field('region'),
            Field('first'),
        )

    def handle(self, request, data):
        # NOTE (majklk): This is a bit of a hack, essentially rewriting this
        # request so that we can chain it as an input to the next view...
        # but hey, it totally works.
        request.method = 'GET'

        first = data.pop('first', None)

        if first:
            data['ordering'] = 0

        return self.next_view.as_view()(request, **data)


class FormRepository(object):
    '''Simple form repository which returns cached classes'''

    _forms = {}

    def get_form(self, cls_name, **kwargs):

        if cls_name not in self._forms:

            model_cls = get_class(cls_name)

            form_class_base = getattr(
                model_cls, 'feincms_item_editor_form', WidgetForm)

            default_widgets = WIDGETS

            model_cls.init_widgets()

            default_widgets.update(getattr(model_cls, 'widgets', {}))

            self._forms[cls_name] = modelform_factory(
                model_cls,
                exclude=[],
                form=form_class_base,
                widgets=default_widgets)

        return self._forms[cls_name]


form_repository = FormRepository()
