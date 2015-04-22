
import operator

import six
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import Field, HTML, Layout
from django import forms
from django.contrib.auth import get_permission_codename
from django.contrib.contenttypes.models import ContentType
from django.forms.models import modelform_factory
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from feincms.admin.item_editor import ItemEditorForm
from horizon.utils.memoized import memoized
from horizon_contrib.common import get_class
from horizon_contrib.forms import SelfHandlingForm, SelfHandlingModelForm
from leonardo.utils.templates import template_choices

WIDGETS = {
            'template_name': forms.RadioSelect(choices=[]),
            'region': forms.widgets.HiddenInput,
            'parent': forms.widgets.HiddenInput,
            'ordering': forms.widgets.HiddenInput,
            }



class WidgetForm(ItemEditorForm, SelfHandlingModelForm):

    id = forms.CharField(
        widget=forms.widgets.HiddenInput,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(WidgetForm, self).__init__(*args, **kwargs)

        queryset = self.fields['content_theme'].queryset

        self.fields['content_theme'].queryset = \
            queryset.filter(widget_class=self._meta.model.__name__)

        self.helper.layout = Layout(
            TabHolder(
                Tab(self._meta.model._meta.verbose_name.capitalize(),
                    *self._meta.model.fields()
                    ),
                Tab('Theme',
                    'base_theme', 'content_theme', 'label', 'id',
                    ),
                Tab('Dimensions',
                    ('region', 'ordering', 'parent'),
                    ),
            )
        )


class WidgetDeleteForm(SelfHandlingForm):

    def handle(self, request, data):
        pass


class WidgetCreatForm(SelfHandlingForm):

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

        from .models import Page
        page = Page.objects.get(id = page_id)

        super(WidgetCreatForm, self).__init__(*args, **kwargs)

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

        """
        render ok, but save not work
        self.helper.layout = Layout(
                HTML(render_to_string("widget/content_type_selection_widget.html", {'grouped': grouped, 'ungrouped': ungrouped})
                ),
            )
        """


    def handle(self, request, data):
        # NOTE (majklk): This is a bit of a hack, essentially rewriting this
        # request so that we can chain it as an input to the next view...
        # but hey, it totally works.
        request.method = 'GET'

        return self.next_view.as_view()(request, **data)

@memoized
def get_widget_update_form(**kwargs):
    """
    widget = get_widget_from_id(widget_id)

    """
    model_cls = get_class(kwargs['cls_name'])

    form_class_base = getattr(
        model_cls, 'feincms_item_editor_form', WidgetForm)

    WidgetModelForm = modelform_factory(model_cls,
                                        exclude=[],
                                        form=form_class_base,
                                        widgets=WIDGETS)

    return WidgetModelForm
