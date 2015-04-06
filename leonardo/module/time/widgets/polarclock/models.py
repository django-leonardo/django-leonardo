import datetime
import pytz
from django.db import models
from django.utils.translation import ugettext_lazy as _
from hrcms.module.boardie.models import WidgetMixin
from hrcms.module.boardie.forms import AngularTextInput, AngularSelect
from crispy_forms.layout import Layout, Fieldset, Field, TabHolder, Tab

class PolarClockWidget(WidgetMixin):
    """
    Widget which shows polar clock.
    """
    time_zone = models.CharField(max_length=127, verbose_name=_('time zone'),choices=[(x, x) for x in pytz.common_timezones], default='Europe/Prague')
    show_day_only = models.BooleanField(verbose_name=_('show day only?'), default=False)

    @classmethod
    def form_fields(self):
        return [
            'name',
            'width',
            'height',
            'update_interval_length',
            'update_interval_unit',
            'time_zone',
        ]

    @classmethod
    def form_widgets(self):
        return {
            'name': AngularTextInput(attrs={'autofocus': True}),
            'width': AngularSelect,
            'height': AngularSelect,
            'update_interval_length': AngularTextInput,
            'update_interval_unit': AngularSelect,
            'time_zone': AngularSelect,
        }

    @classmethod
    def form_layout(self):
        return TabHolder(
            Tab('Text',
                'name',
                'time_zone',
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
            'global_time': datetime.datetime.now().isoformat(),
            'local_time': datetime.datetime.now().isoformat(),
            'time_zone': self.time_zone
        }
        return data

    class Meta:
        abstract = True
        verbose_name = _("polar clock")
        verbose_name_plural = _("polar clocks")
