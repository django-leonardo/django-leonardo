# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from leonardo.module.web.models import Widget


ON_CLICK_CHOICES = (
    ('open_modal', _('open in modal window')),
    ('go_to_page', _('go to linked page')),
)

SIZE_CHOICES = (
    ('small', _('small')),
    ('medium', _('medium')),
    ('large', _('large')),
)

ALIGN_CHOICES = (
    ('left', _('left')),
    ('right', _('right')),
)


class SimpleImageWidget(Widget):

    image = models.ForeignKey("media.Image", verbose_name=_("image"), related_name="%(app_label)s_%(class)s_images")
    size = models.CharField(max_length=255, verbose_name=_("size"), choices=SIZE_CHOICES, blank=True)
    on_click = models.CharField(max_length=255, verbose_name=_("on click action"), choices=ON_CLICK_CHOICES, blank=True)
    alignment = models.CharField(max_length=255, verbose_name=_("alignment"), choices=ALIGN_CHOICES, default='left')

    def get_size(self):
        if self.size == 'small':
            return '96x96'
        elif self.size == 'medium':
            return '256x256'
        else:
            return '768x768'

    class Meta:
        abstract = True
        verbose_name = _("simple image")
        verbose_name_plural = _('simple images')
