# -#- coding: utf-8 -#-

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from leonardo.module.web.models import Widget

ON_CLICK_CHOICES = (
    ('open_modal', _('open in modal window')),
    ('open_new_window', _('open new window')),
    ('on_page', _('disply in page')),
)

SIZE_CHOICES = (
    ('small', _('small')),
    ('medium', _('medium')),
    ('large', _('large')),
)


class SimpleImageWidget(Widget):

    image = models.ForeignKey("media.Image", verbose_name=_("image"), related_name="%(app_label)s_%(class)s_images")
    size = models.CharField(max_length=255, verbose_name=_("size"), choices=SIZE_CHOICES, blank=True)
    detail = models.CharField(max_length=255, verbose_name=_("on click action"), choices=ON_CLICK_CHOICES, blank=True)

    def get_size(self):
        return getattr(settings,
                       'MEDIA_THUMB_%s_GEOM' % self.size.upper(),
                       '96x96')

    class Meta:
        abstract = True
        verbose_name = _("simple image")
        verbose_name_plural = _('simple images')
