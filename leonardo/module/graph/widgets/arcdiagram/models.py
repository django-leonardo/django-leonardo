import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from hrcms.module.boardie.forms import AngularTextInput, AngularSelect
from hrcms.module.graph.models import GraphWidgetMixin
from crispy_forms.layout import TabHolder, Tab

ARC_POSITION_CHOICES = (
    ('above', _('above nodes')),
    ('below', _('below nodes')),
    ('both', _('both')),
)

class ArcDiagramWidget(GraphWidgetMixin):
    """
    Widget which shows arc diagram.
    """
    arc_position = models.CharField(max_length=32, verbose_name=_('edges position'), default="below", choices=ARC_POSITION_CHOICES)

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
        if self.source.type == 'dummy':
            data = self.source.get_dummy_data()
        else:
            data = {}
        data['arc_position'] = self.arc_position
        return data

    class Meta:
        abstract = True
        verbose_name = _("arc diagram")
        verbose_name_plural = _("arc diagrams")
