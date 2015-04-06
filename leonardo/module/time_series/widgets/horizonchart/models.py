import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _

from boardie.module.time_series.models import TimeSeriesSource, TimeSeriesWidgetMixin
from boardie.forms import AngularTextInput, AngularSelect
from crispy_forms.layout import Layout, Fieldset, Field, TabHolder, Tab

class HorizonChartWidget(TimeSeriesWidgetMixin):
    """
    Widget which shows horizon chart.
    """
    horizon_folds = models.IntegerField(verbose_name=_('horizon folds'), default=4)

    @classmethod
    def form_fields(self):
        return [
            'name',
            'width',
            'height',
            'update_interval_length',
            'update_interval_unit',
            'horizon_folds'
        ]

    @classmethod
    def form_widgets(self):
        return {
            'name': AngularTextInput(attrs={'autofocus': True}),
            'width': AngularSelect,
            'height': AngularSelect,
            'update_interval_length': AngularTextInput,
            'update_interval_unit': AngularSelect,
        }

    @classmethod
    def form_layout(self):
        return TabHolder(
            Tab('Text',
                'name',
            ),
            Tab('Size',
                'width',
                'height',
                'update_interval_length',
                'update_interval_unit',
            ),
        )

    def widget_data(self, request):
        data = {
            'metrics': self.get_metrics(),
            'step_seconds': 60,#int(self.get_step_delta().total_seconds),
            'low_horizon': self.low_horizon,
            'high_horizon': self.high_horizon,
            'host': self.get_host()
        }
        return data

    class Meta:
        abstract = True
        verbose_name = _("horizon chart")
        verbose_name_plural = _("horizon charts")
