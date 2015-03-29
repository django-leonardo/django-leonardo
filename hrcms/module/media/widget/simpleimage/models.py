# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from webcms.models import Widget

from webcms.module.media.models import File 
#from webcms.module.media.fields import MediaFileForeignKey

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
    image = models.ForeignKey(File, verbose_name=_("image"), limit_choices_to={'type': 'image'})
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
