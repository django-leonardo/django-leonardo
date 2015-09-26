
from django.db import models
from django.utils.translation import ugettext_lazy as _
from leonardo.fields import SimpleSelect2Widget
from leonardo.module.media.fields import VectorField
from leonardo.module.media.models import Vector
from leonardo.module.web.models import Widget
from leonardo.module.web.widgets.forms import WidgetUpdateForm


class VectorForm(WidgetUpdateForm):

    source = VectorField(widget=SimpleSelect2Widget())


class VectorGraphicsWidget(Widget):

    feincms_item_editor_form = VectorForm

    icon = "fa fa-area-chart"

    source = models.ForeignKey(Vector, related_name="%(app_label)s_%(class)s_related")

    class Meta:
        abstract = True
        verbose_name = _('Vector graphics')
        verbose_name_plural = _('Vector graphics')
