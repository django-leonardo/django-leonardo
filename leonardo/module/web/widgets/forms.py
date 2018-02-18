
import copy

import floppyforms
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import HTML, Field, Fieldset, Layout
from django import forms
from django.apps import apps
from leonardo.module.web.models import Page
from django.forms.models import modelform_factory
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import Select2Widget
from feincms.admin.item_editor import ItemEditorForm
from horizon_contrib.common import get_class
from leonardo.forms import SelfHandlingForm, SelfHandlingModelForm
from leonardo.module.web.page.fields import PageSelectField
from leonardo.utils.widgets import get_grouped_widgets
from django.template.loader import render_to_string


class IconPreviewSelect(floppyforms.widgets.Select):
    template_name = 'floppyforms/select_preview.html'


WIDGETS = {
    'template_name': forms.RadioSelect(choices=[]),
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

    prerendered_content = forms.CharField(
        label=_("CSS Classes"), help_text=_("Custom CSS classes"),
        required=False)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        model = kwargs.pop('model', None)

        super(WidgetForm, self).__init__(*args, **kwargs)

        if isinstance(model, Page):
            self.fields['parent'] = PageSelectField(
                label=_("Parent"), help_text=_("Parent Page"))
        else:
            self.fields['parent'].widget = forms.widgets.HiddenInput()

        initial = kwargs.get('initial', None)

        if initial and initial.get('id', None):
            widget = self._meta.model.objects.get(
                id=initial['id'])
            data = widget.dimensions

            self.init_content_themes()

        elif 'instance' in kwargs:
            widget = kwargs['instance']
            data = widget.dimensions

            self.init_content_themes()
        else:
            data = []
            widget = None

            # set defaults and delete id field
            self.init_themes()
            del self.fields['id']

        # get all fields for widget
        main_fields = self._meta.model.fields()
        main_fields.update({'label': 'label'})
        main_fields.pop("parent", None)

        self.helper.layout = Layout(
            TabHolder(
                Tab(self._meta.model._meta.verbose_name.capitalize(),
                    *self.get_main_fields(main_fields),
                    css_id='field-{}'.format(slugify(self._meta.model))
                    ),
                Tab(_('Styles'),
                    'base_theme', 'content_theme', 'color_scheme',
                    'prerendered_content',
                    Fieldset(_('Positions'), 'layout', 'align',
                             'vertical_align', 'parent'),
                    *self.get_id_field(),
                    css_id='theme-widget-settings'
                    ),
                Tab(_('Effects'),
                    'enter_effect_style', 'enter_effect_duration',
                    'enter_effect_delay', 'enter_effect_offset',
                    #'enter_effect_iteration',
                    css_id='theme-widget-effects'
                    ),
            ),
            HTML(render_to_string('widget/_update_preview.html',
                                  {'class_name': ".".join([
                                      self._meta.model._meta.app_label,
                                      self._meta.model._meta.model_name])
                                   }))

        )

        self.fields['label'].widget = forms.TextInput(
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

    def get_id_field(self):
        if 'id' in self.fields:
            return ['id']
        return []

    def init_content_themes(self):
        # filter content themes by widget
        queryset = self.fields['content_theme'].queryset
        self.fields['content_theme'].queryset = \
            queryset.filter(widget_class=self._meta.model.__name__)

    def init_themes(self):
        queryset = self.fields['content_theme'].queryset

        self.fields['content_theme'].queryset = queryset.filter(
            widget_class=self._meta.model.__name__)

        try:
            base_theme = self.fields['base_theme'].queryset.get(
                name__icontains='default')
        except:
            self.fields['base_theme'].initial = self.fields[
                'base_theme'].queryset.first()
        else:
            self.fields['base_theme'].initial = base_theme

        try:
            content_theme = self.fields['content_theme'].queryset.get(
                name__icontains='default')
        except:
            self.fields['content_theme'].initial = self.fields[
                'content_theme'].queryset.first()
        else:
            self.fields['content_theme'].initial = content_theme


class WidgetUpdateForm(WidgetForm):

    '''obsolete name'''

    pass


class WidgetMoveForm(SelfHandlingModelForm):

    '''Widget move form'''

    parent = PageSelectField(
        label=_('Page')
    )

    region = forms.ChoiceField(
        label=_('Region'),
        widget=Select2Widget()
    )

    def __init__(self, *args, **kwargs):

        super(WidgetMoveForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name not in ['parent', 'region']:
                field.widget = forms.widgets.HiddenInput()

        # load template regions
        self.fields['region'].choices = [(str(region.key),
                                          '%s%s' % (
            str(region.title),
            ' - Inherited' if region.inherited else ''))
            for region in self.instance.parent.template.regions]

    class Meta:
        widgets = {}


class WidgetCreateForm(WidgetUpdateForm):

    ''''''

    pass


class WidgetDeleteForm(SelfHandlingForm):

    def handle(self, request, data):
        pass


class WidgetSelectForm(SelfHandlingForm):

    cls_name = forms.ChoiceField(
        label=_("Widget Type"),
        choices=[],
        required=True,
        widget=Select2Widget()
    )

    first = forms.BooleanField(
        label=_('First ?'),
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
        label=_('Region'),
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
        self.fields['region'].choices = [(str(region.key),
                                          '%s%s' % (
            str(region.title),
            _(' - Inherited') if region.inherited else ''))
            for region in feincms_object.template.regions]

        if region_name:
            self.fields['ordering'].initial = len(
                getattr(feincms_object.content, region_name, [])) + 1

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

    def get_generic_form(self, cls_name, form_cls, widgets={}, **kwargs):
        model_cls = get_class(cls_name)
        return modelform_factory(
            model_cls,
            exclude=[],
            form=form_cls,
            widgets=widgets)

form_repository = FormRepository()
