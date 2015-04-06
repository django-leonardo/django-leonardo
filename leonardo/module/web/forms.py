
from django.forms.models import modelform_factory

from webcms.models import DEFAULT_DISPLAY_OPTIONS
from webcms.forms import GenericWidgetModelForm, WidgetOptionsForm
from webcms.utils.forms import process_dajax_data
from webcms.utils.widgets import get_widget_from_id, get_widget_class_from_id

def get_widget_update_forms(request, widget_id, set_initial, data=None):
    widget = get_widget_from_id(widget_id)
    model_cls = get_widget_class_from_id(widget_id)

    form_class_base = getattr(model_cls, 'feincms_item_editor_form', GenericWidgetModelForm)

    WidgetModelForm = modelform_factory(model_cls,
        exclude=('parent', 'region', 'ordering'),
        form=form_class_base,)
#        formfield_callback=curry(self.formfield_for_dbfield, request=request))

    del WidgetModelForm.base_fields['region']
    del WidgetModelForm.base_fields['ordering']

    if set_initial:
        try:
            initial = widget.options
            dim = initial.pop('size')
            pad = initial.pop('padding')
            mar = initial.pop('margin')
            aln = initial.pop('align')
        except:
            initial = DEFAULT_DISPLAY_OPTIONS.copy()
            dim = initial.pop('size')
            pad = initial.pop('padding')
            mar = initial.pop('margin')
            aln = initial.pop('align')

        initial['span'] = dim[0]
        initial['vertical_span'] = dim[1]
        initial['append'] = pad[1]
        initial['vertical_append'] = pad[2]
        initial['prepend'] = pad[3]
        initial['vertical_prepend'] = pad[0]
        initial['push'] = mar[1]
        initial['vertical_push'] = mar[2]
        initial['pull'] = mar[3]
        initial['vertical_pull'] = mar[0]
        initial['align'] = aln[0]
        initial['vertical_align'] = aln[1]

    if data == None:
        form = WidgetOptionsForm(initial=initial)
        obj_form = WidgetModelForm(instance=widget, prefix='obj-form')
    else:
        form = WidgetOptionsForm(data)
        obj_form = WidgetModelForm(data=data,instance=widget, prefix='obj-form')

    return form, obj_form
