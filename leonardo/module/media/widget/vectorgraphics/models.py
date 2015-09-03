
from django.utils.translation import ugettext_lazy as _
from django.db import models

from leonardo.module.media.models import Vector

from leonardo.module.web.models import Widget


class VectorGraphicsWidget(Widget):

    icon = "fa fa-area-chart"

    source = models.ForeignKey(Vector, related_name="%(app_label)s_%(class)s_related")

    class Meta:
        abstract = True
        verbose_name = _('Vector graphics')
        verbose_name_plural = _('Vector graphics')
