# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from webcms.models import Widget

class StreamPlayerWidget(Widget):
    source = models.URLField(_('stream link'),
        help_text=_('This should be a link to a streamed audio.'))

    class Meta:
        abstract = True
        verbose_name = _('stream player')
        verbose_name_plural = _('stream players')
