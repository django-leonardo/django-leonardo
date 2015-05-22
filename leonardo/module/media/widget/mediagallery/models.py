# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from leonardo.module.web.models import Widget

DETAIL_CHOICES = (
    ('modal', _('modal window')),
    ('link', _('link to file')),
    ('page', _('on page')),
)

SIZE_CHOICES = (
    ('96x96', _('small')),
    ('128x128', _('medium')),
    ('386x386', _('large')),
)

class MediaGalleryWidget(Widget):
    category = models.ForeignKey('media.LeonardoFolder', verbose_name=_("Directory"), related_name="%(app_label)s_%(class)s_categories")
    size = models.CharField(max_length=255, verbose_name=_("thumbnail size"), choices=SIZE_CHOICES, default='96x96')
    detail = models.CharField(max_length=255, verbose_name=_("detail view"), choices=DETAIL_CHOICES, default='modal')

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
