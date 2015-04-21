
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


class WidgetForm(ItemEditorForm):

    """
    theme = forms.ChoiceField(
        choices=[],
        widget=forms.RadioSelect,
    )
    """

    parent = forms.CharField(
        widget=forms.widgets.HiddenInput,
    )

    class Meta:

        widgets = WIDGETS

    """
    def __init__(self, *args, **kwargs):
        super(WidgetForm, self).__init__(*args, **kwargs)

        items = self._meta.model.templates()
        choices = template_choices(items, suffix=True)
        if not items:
            items.insert(0, ("", _("No Template available")))

        self.fields['theme'].choices = choices

        self.helper.layout = Layout(
            TabHolder(
                Tab('Main',
                    *self._meta.model.fields()
                    ),
                Tab('Theme',
                    'theme', 'label',
                    ),


            )
        )
    """


@memoized
def get_widget_update_form(**kwargs):
    """
    widget = get_widget_from_id(widget_id)

    """
    model_cls = get_class(kwargs['cls_name'])

    form_class_base = getattr(
        model_cls, 'feincms_item_editor_form', WidgetForm)

    WidgetModelForm = modelform_factory(model_cls,
                                        exclude=(
                                            'parent', 'region', 'ordering'),
                                        form=form_class_base,
                                        widgets=WIDGETS)

    return WidgetModelForm
