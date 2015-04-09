
from django.apps import AppConfig

from .widget import *


default_app_config = 'leonardo.module.web.WebConfig'

from .widget.angulargauge.models import AngularGaugeWidget

class Default(object):

    optgroup = 'Web'

    @property
    def middlewares(self):
        return [
            'leonardo.module.web.middleware.WebMiddleware',
        ]

    @property
    def apps(self):
        return [
            'leonardo.module.timeseries',
        ]

    @property
    def widgets(self):
        return [
            AngularGaugeWidget,
        ]


class TimeSeriesConfig(AppConfig, Default):
    name = 'leonardo.module.timeseries'
    verbose_name = "TimeSeries"


default = Default()
