# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from webcms.models import Widget

from webcms.module.media.models import Category 

DETAIL_CHOICES = (
    ('modal', _('modal window')),
    ('link', _('link to file')),
    ('page', _('on page')),
)

SIZE_CHOICES = (
    ('small', _('small')),
    ('medium', _('medium')),
    ('large', _('large')),
)

class MediaGalleryWidget(Widget):
    category = models.ForeignKey(Category, verbose_name=_("files"))
    size = models.CharField(max_length=255, verbose_name=_("thumbnail size"), choices=SIZE_CHOICES, default='small')
    detail = models.CharField(max_length=255, verbose_name=_("detail view"), choices=DETAIL_CHOICES, default='modal')

    def get_size(self):
        if self.size == 'small':
            return '96x96'
        elif self.size == 'medium':
            return '128x128'
        else:
            return '386x386'

    def thumb_geom(self):
        if self.size == 'small':
            return '96x96'
        elif self.size == 'medium':
            return '128x128'
        else:
            return '256x256'

    def image_geom(self):
        return '800x800'

    class Meta:
        abstract = True
        verbose_name = _("media gallery")
        verbose_name_plural = _('media galleries')
