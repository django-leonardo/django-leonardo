import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _

from yamlfield.fields import YAMLField

from feincms.module.medialibrary.models import MediaFile

from boardie.module.time_series.models import TimeSeriesWidgetMixin
from boardie.forms import AngularTextInput, AngularSelect, AngularTextarea
from crispy_forms.layout import Layout, Fieldset, Field, TabHolder, Tab

class SystemChartWidget(TimeSeriesWidgetMixin):
    """
    Widget which shows system chart.
    """

    align_to_from = models.BooleanField(verbose_name=_('align to from'), default=False)
    background_url = models.CharField(max_length=255, verbose_name=_('background image'), blank=True, null=True, help_text=_('Absolute or relative URL for backgound image'))
 #   visualizations = YAMLField(verbose_name=_("visualizations"), default='visualizations:[]', help_text=_('Visual settings for metrics'))

    @classmethod
    def form_fields(self):
        return [
            'name',
            'width',
            'height',
            'update_interval_length',
            'update_interval_unit',
            'background_url',
            'metrics',
#            'visualizations',
        ]

    @classmethod
    def form_widgets(self):
        return {
            'name': AngularTextInput(attrs={'autofocus': True}),
            'width': AngularSelect,
            'height': AngularSelect,
            'update_interval_length': AngularTextInput,
            'update_interval_unit': AngularSelect,
            'background_url': AngularTextInput,
            'metrics': AngularTextarea,
#            'visualizations': AngularTextarea,
        }

    @classmethod
    def form_layout(self):
        return TabHolder(
            Tab('Basics',
                'name',
                'background_url',
            ),
            Tab('Metrics',
                'metrics',
            ),
#            Tab('Visualizations',
#                'visualizations',
#            ),
            Tab('Display',
                'width',
                'height',
                'update_interval_length',
                'update_interval_unit',
            ),
        )

    def widget_data(self, request):
        values = self.get_graphite_last_values()
#        viz = self.visualizations
#        for value in values:
#            value['type'] = viz[value.get('device')]['type']
#            value['y'] = viz[value.get('device')]['y']
#            value['x'] = viz[value.get('device')]['x']
        return values

    class Meta:
        abstract = True
        verbose_name = _("system chart")
        verbose_name_plural = _("system charts")
