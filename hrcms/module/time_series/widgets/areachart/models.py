import datetime
import time

from django.db import models
from django.utils.translation import ugettext_lazy as _

from boardie.module.time_series.models import TimeSeriesSource, TimeSeriesWidgetMixin
from boardie.forms import AngularTextInput, AngularSelect
from crispy_forms.layout import TabHolder, Tab, Field

OFFSET_CHOICES = (
    ('stacked', _('stacked')), 
    ('stream', _('stream')), 
    ('expanded', _('expanded')),
)

class AreaChartWidget(TimeSeriesWidgetMixin):
    """
    Widget which shows area chart.
    """

    offset = models.CharField(max_length=55, verbose_name=_("offset"), default='stacked', choices=OFFSET_CHOICES)
    align_to_from = models.BooleanField(verbose_name=_('align to from'), default=False)

    @classmethod
    def form_fields(self):
        return [
            'name',
            'width',
            'height',
            'update_interval_length',
            'update_interval_unit',
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
        end = self.relative_start() + self.get_duration_delta()

        data = {
            'metrics': self.get_metrics(),
            'step_seconds': self.get_step_delta().total_seconds(),
            'step_fun': self.step_fun,
            'low_horizon': self.low_horizon,
            'high_horizon': self.high_horizon,
            'start': str(long(time.mktime(self.relative_start().timetuple()))),
            'end': str(long(time.mktime(end.timetuple()))),
            'host': self.get_host()
        }
        return data

    class Meta:
        abstract = True
        verbose_name = _("area chart")
        verbose_name_plural = _("area charts")
