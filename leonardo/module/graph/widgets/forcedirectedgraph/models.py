import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from hrcms.module.boardie.forms import AngularTextInput, AngularSelect
from hrcms.module.graph.models import GraphWidgetMixin
from crispy_forms.layout import TabHolder, Tab

class ForceDirectedGraphWidget(GraphWidgetMixin):
    """
    Widget which shows force directed graph.
    """
    gravity = models.DecimalField(verbose_name=_('gravity'), default=.05, max_digits=6, decimal_places=2)
    distance = models.IntegerField(verbose_name=_('distance'), default=100)
    charge = models.IntegerField(verbose_name=_('charge'), default=-100) 

    @classmethod
    def form_fields(self):
        return [
            'name',
            'width',
            'height',
            'update_interval_length',
            'update_interval_unit',
            'graph_source'
        ]

    @classmethod
    def form_widgets(self):
        return {
            'name': AngularTextInput(attrs={'autofocus': True}),
            'width': AngularSelect,
            'height': AngularSelect,
            'update_interval_length': AngularTextInput,
            'update_interval_unit': AngularSelect,
            'graph_source': AngularSelect,
        }

    @classmethod
    def form_layout(self):
        return TabHolder(
            Tab('Text',
                'name',
                'graph_source',
            ),
            Tab('Size',
                'width',
                'height',
                'update_interval_length',
                'update_interval_unit',
            ),
        )

    def widget_data(self, request):
        if self.source.type == 'dummy':
            return self.source.get_dummy_data()
        return data

    class Meta:
        abstract = True
        verbose_name = _("force directed graph")
        verbose_name_plural = _("force directed graphs")
