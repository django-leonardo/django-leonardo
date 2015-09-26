# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from leonardo.fields import SimpleSelect2Widget
from leonardo.module.media.fields import VideoField
from leonardo.module.web.models import Widget
from leonardo.module.web.widgets.forms import WidgetUpdateForm


class VideoForm(WidgetUpdateForm):

    video = VideoField(widget=SimpleSelect2Widget())


class SimpleVideoWidget(Widget):

    feincms_item_editor_form = VideoForm

    icon = "fa fa-video-camera"

    thumb = models.ForeignKey("media.Image", verbose_name=_(
        "thumbnail"), blank=True, null=True, related_name="%(app_label)s_%(class)s_thumbnails")
    video = models.ForeignKey(
        "media.Video", verbose_name=_("video"), related_name="%(app_label)s_%(class)s_videos")
    width = models.IntegerField(verbose_name=_("width"), default=100)
    height = models.IntegerField(verbose_name=_("height"), default=100)

    class Meta:
        abstract = True
        verbose_name = _("simple video")
        verbose_name_plural = _('simple video')
