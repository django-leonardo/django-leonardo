import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _

from boardie.module.time_series.models import TimeSeriesSource, TimeSeriesWidgetMixin
from boardie.forms import AngularTextInput, AngularSelect
from crispy_forms.layout import Layout, Fieldset, Field, TabHolder, Tab

class AngularGaugeWidget(TimeSeriesWidgetMixin):
    """
    Widget which shows angular gauge.
    """
    major_ticks = models.IntegerField(verbose_name=_('major ticks'), default=5)
    minor_ticks = models.IntegerField(verbose_name=_('minor ticks'), default=2)
    threshold_warning = models.IntegerField(verbose_name=_('warning threshold'), default=70)
    threshold_critical = models.IntegerField(verbose_name=_('critical threshold'), default=90)

    @classmethod
    def form_fields(self):
        return [
            'name',
            'width',
            'height',
            'update_interval_length',
            'update_interval_unit',
            'major_ticks',
            'minor_ticks',
            'threshold_warning',
            'threshold_critical',
            'low_horizon',
            'high_horizon'
        ]

    @classmethod
    def form_widgets(self):
        return {
            'name': AngularTextInput(attrs={'autofocus': True}),
            'width': AngularSelect,
            'height': AngularSelect,
            'update_interval_length': AngularTextInput,
            'update_interval_unit': AngularSelect,
            'major_ticks': AngularTextInput,
            'minor_ticks': AngularTextInput,
            'threshold_warning': AngularTextInput,
            'threshold_critical': AngularTextInput,
            'low_horizon': AngularTextInput,
            'high_horizon': AngularTextInput,
        }

    @classmethod
    def form_layout(self):
        return TabHolder(
            Tab('Text',
                'name',
                'major_ticks',
                'minor_ticks',
                'threshold_warning',
                'threshold_critical',
                'low_horizon',
                'high_horizon'
            ),
            Tab('Size',
                'width',
                'height',
                'update_interval_length',
                'update_interval_unit',
            ),
        )

    def widget_data(self, request):
        return self.get_graphite_last_value()

    class Meta:
        abstract = True
        verbose_name = _("angular gauge")
        verbose_name_plural = _("angular gauges")
