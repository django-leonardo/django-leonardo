
import copy
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import Field, HTML, Layout, Fieldset
from django import forms
import floppyforms
from django.db.models.loading import get_model
from django.forms.models import modelform_factory
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from feincms.admin.item_editor import ItemEditorForm
from horizon.utils.memoized import memoized
from horizon_contrib.common import get_class
from leonardo.forms import SelfHandlingForm, SelfHandlingModelForm
from leonardo.utils.widgets import get_grouped_widgets
from .fields import get_widget_select_field


class IconPreviewSelect(floppyforms.widgets.Select):
    template_name = 'floppyforms/select_preview.html'


WIDGETS = {
    'template_name': forms.RadioSelect(choices=[]),
    'parent': forms.widgets.HiddenInput,
    'ordering': forms.widgets.HiddenInput,
    'icon': IconPreviewSelect(attrs={'style': "font-family: 'FontAwesome', Helvetica;"}),
}


class WidgetUpdateForm(ItemEditorForm, SelfHandlingModelForm):

    '''Widget Create/Update Form'''

    id = forms.CharField(
        widget=forms.widgets.HiddenInput,
        required=False
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(WidgetUpdateForm, self).__init__(*args, **kwargs)

        if request:
            queryset = self.fields['content_theme'].queryset

            self.fields['content_theme'].queryset = \
                queryset.filter(widget_class=self._meta.model.__name__)
        else:
            # set defaults
            self.init_themes()
            del self.fields['id']

        # get all fields for widget
        main_fields = self._meta.model.fields()
        main_fields.update({'label': 'label'})
        self.helper.layout = Layout(
            TabHolder(
                Tab(self._meta.model._meta.verbose_name.capitalize(),
                    *main_fields,
                    css_id='field-{}'.format(slugify(self._meta.model))
                    ),
                Tab(_('Theme'),
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
            from .tables import WidgetDimensionTable
            _request = copy.copy(request)
            _request.POST = {}
            _request.method = 'GET'
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
        required=True
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
        feincms_cls_name = kwargs.pop('cls_name', None)
        self.next_view = kwargs.pop('next_view', None)

        module, cls = feincms_cls_name.split('.')
        ObjectCls = get_model(module, cls)
        feincms_object = ObjectCls.objects.get(id=page_id)

        super(WidgetSelectForm, self).__init__(*args, **kwargs)

        self.fields['page_id'].initial = feincms_object.id
        self.fields['region'].initial = region_name
        self.fields['ordering'].initial = \
            len(getattr(feincms_object.content, region_name, [])) + 1
        self.fields['parent'].initial = feincms_object.id

        choices, grouped, ungrouped = get_grouped_widgets(
            feincms_object, request)

        # reduce choices for validation
        self.fields['cls_name'] = get_widget_select_field(feincms_object)
        self.fields['cls_name'].choices = [(str(choice[0]), str(choice[1]))
                                           for choice in choices]

        # for now ungrouped to grouped
        grouped['Web'] = ungrouped + grouped.get('Web', [])

        self.helper.layout = Layout(
            Field('region'),
            Field('parent'),
            Field('page_id'),
            Field('ordering'),
            'cls_name',
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
