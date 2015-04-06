import datetime
import time

from django.db import models
from django.utils.translation import ugettext_lazy as _

from boardie.module.time_series.models import TimeSeriesSource, TimeSeriesWidgetMixin
from boardie.forms import AngularTextInput, AngularSelect, AngularTextarea
from crispy_forms.layout import TabHolder, Tab, Field

DOMAIN_CHOICES = (
    ('hour', _('hours')),
    ('day', _('days')), 
    ('week', _('week')), 
    ('month', _('month')), 
    ('year', _('year')), 
)

SUBDOMAIN_CHOICES = (
    ('min', _('minutes')),
    ('hour', _('hours')),
    ('day', _('days')), 
    ('week', _('week')), 
    ('month', _('month')), 
    ('year', _('year')), 
)

ORIENTATION_CHOICES = (
    ('topbottom', _('top to bottom')),
    ('leftright', _('left to right')),
)

class CalendarHeatMapWidget(TimeSeriesWidgetMixin):
    """
    Widget which shows calendar heat map.
    """

    domain = models.CharField(max_length=55, verbose_name=_("domain"), default='day', choices=DOMAIN_CHOICES)
    subdomain = models.CharField(max_length=55, verbose_name=_("subdomain"), default='hour', choices=SUBDOMAIN_CHOICES)
    orientation = models.CharField(max_length=55, verbose_name=_("orientation"), default='linear', choices=ORIENTATION_CHOICES)
    domain_range = models.IntegerField(verbose_name=_("range"), default=24, help_text=_('Number of domains to display.'))

    @classmethod
    def form_fields(self):
        return [
            'name',
            'width',
            'height',
            'update_interval_length',
            'update_interval_unit',
            'domain',
            'subdomain',
            'domain_range',
            'time_series_source',
            'metrics',
        ]

    @classmethod
    def form_widgets(self):
        return {
            'name': AngularTextInput(attrs={'autofocus': True}),
            'width': AngularSelect,
            'height': AngularSelect,
            'update_interval_length': AngularTextInput,
            'update_interval_unit': AngularSelect,
            'domain': AngularSelect,
            'subdomain': AngularSelect,
            'domain_range': AngularTextInput,
            'time_series_source': AngularSelect,
            'metrics': AngularTextarea,
        }

    @classmethod
    def form_layout(self):
        return TabHolder(
            Tab('Basic',
                'name',
                'domain',
                'subdomain',
                'domain_range',
            ),
            Tab('Metrics',
                'time_series_source',
                'metrics',
            ),
            Tab('Size',
                'width',
                'height',
                'update_interval_length',
                'update_interval_unit',
            ),
        )

    def widget_data(self, request):
        values = self.get_graphite_values()[0]['values']
        cal_values = {}
        for value in values:
            cal_values[value[1]] = value[0]
        return {
            'values': cal_values,
            'start': time.time() - self.get_duration_delta().total_seconds()
        } # January 15, 2000 @15:36

    def save(self):
        self.duration_length = self.domain_range
        self.duration_unit = self.domain
        self.step_length = 1
        self.step_unit = self.subdomain
        super(CalendarHeatMapWidget, self).save()

    class Meta:
        abstract = True
        verbose_name = _("calendar heat map")
        verbose_name_plural = _("calendar heat maps")
