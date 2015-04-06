# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from webcms.models import Widget

from webcms.module.media.models import File 

class SimpleVideoWidget(Widget):
    thumb = models.ForeignKey(File, verbose_name=_("thumbnail"), limit_choices_to={'type': 'image'}, blank=True, null=True, related_name='simple_video_thumb')
    video = models.ForeignKey(File, verbose_name=_("video"), related_name='simple_video_video')
    width = models.IntegerField(verbose_name=_("width"), default=100)
    height = models.IntegerField(verbose_name=_("height"), default=100)

    class Meta:
        abstract = True
        verbose_name = _("simple video")
        verbose_name_plural = _('simple video')
