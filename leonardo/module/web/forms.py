
import operator

from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import Field, Layout
from django import forms
from django.forms.models import modelform_factory
from django.utils.translation import ugettext_lazy as _
from feincms.admin.item_editor import ItemEditorForm
from horizon.utils.memoized import memoized
from horizon_contrib.common import get_class
from horizon_contrib.forms import SelfHandlingModelForm
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
    )

    def __init__(self, *args, **kwargs):
        super(WidgetForm, self).__init__(*args, **kwargs)

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
