# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from webcms.models import Widget

from webcms.module.media.models import File

VERSION_CHOICES = (
    ('10.0.0', _('version 10 and newer')),
    ('9.0.0', _('version 9 and newer')),
)

VARS_DEFAULT = """var vars = {
}
"""

PARAMS_DEFAULT = """var params = {
}
"""

ATTRS_DEFAULT = """var attrs = {
}
"""

class FlashObjectWidget(Widget):
    file = models.ForeignKey(File, verbose_name=_("flash file"), limit_choices_to={'type': 'swf'} )
    version = models.CharField(max_length=255, verbose_name=_("flash version"), choices=VERSION_CHOICES)
    width = models.CharField(max_length=255, verbose_name=_("width"), default='640')
    height = models.CharField(max_length=255, verbose_name=_("height"), default='480')
    vars = models.TextField(verbose_name=_("variables"), default=VARS_DEFAULT)
    params = models.TextField(verbose_name=_("parameters"), default=PARAMS_DEFAULT)
    attrs = models.TextField(verbose_name=_("attributes"), default=ATTRS_DEFAULT)

    class Meta:
        abstract = True
        verbose_name = _("flash object")
        verbose_name_plural = _('flash objects')
