# -#- coding: utf-8 -#-

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from leonardo.module.web.models import Widget
from leonardo.module.media.fields.image import ImageField

from leonardo.module.web.widgets.forms import WidgetUpdateForm

ON_CLICK_CHOICES = (
    ('open_modal', _('Open in modal window')),
    ('open_new_window', _('Open new window')),
    ('on_page', _('Display in page')),
)

SIZE_CHOICES = (
    ('small', _('small')),
    ('medium', _('medium')),
    ('large', _('large')),
)


class ImageForm(WidgetUpdateForm):

    image = ImageField()


class SimpleImageWidget(Widget):

    icon = "fa fa-file-image-o"

    feincms_item_editor_form = ImageForm

    image = models.ForeignKey(
        "media.Image", verbose_name=_("image"), related_name="%(app_label)s_%(class)s_images")
    size = models.CharField(
        max_length=255, verbose_name=_("size"), choices=SIZE_CHOICES, blank=True)
    detail = models.CharField(max_length=255, verbose_name=_(
        "on click action"), choices=ON_CLICK_CHOICES, blank=True)

    def get_size(self):
        return getattr(settings,
                       'MEDIA_THUMB_%s_GEOM' % self.size.upper(),
                       '96x96')

    def get_template_data(self, *args, **kwargs):
        '''Add size to context'''
        return {'size': self.get_size()}

    class Meta:
        abstract = True
        verbose_name = _("simple image")
        verbose_name_plural = _('simple images')
