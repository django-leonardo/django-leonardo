from django.utils.translation import ugettext_lazy as _
from django_select2.fields import AutoSelect2TagField
from django_select2.views import NO_ERR_RESP
from leonardo.fields import SimpleSelect2Widget
from leonardo.utils.widgets import get_grouped_widgets


def get_widget_select_field(feincms_object):

    class SelectField(AutoSelect2TagField):

        """returns list of plugins from github group or pypi
        """

        def to_python(self, value):
            return value

        def __init__(self, **kwargs):
            self.feincms_object = kwargs.pop('feincms_object')
            super(SelectField, self).__init__(**kwargs)

        search_fields = ['tag__icontains', ]

        def get_field_values(self, value):
            return {'tag': value}

        def get_results(self, request, term, page, context):

            choices, grouped, ungrouped = get_grouped_widgets(self.feincms_object)

            res = [
                (
                    str(cls[0]),
                    str(cls[1]).capitalize(),
                    {}
                )
                for cls in choices if term in str(cls)
            ]

            return NO_ERR_RESP, False, res

    new_type = type(
        'WidgetSelectField', (SelectField,), {})

    return new_type(
        label=_('Widget'),
        widget=SimpleSelect2Widget(),
        feincms_object=feincms_object)
