from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from PIL import Image
import mimetypes
import utils
import os

from feincms.translations import TranslatedObjectMixin, Translation, TranslatedObjectManager

from hrcms.module.media.models import File


class Slot(models.Model):
    name = models.CharField(max_length=255)
    limit = models.PositiveIntegerField(null=True, blank=True)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return None
#        return reverse('banners_slotshow', args=[self.pk])

    def __unicode__(self):
        return 'Banner Slot "%s"' % self.name

    @property
    def published_banners(self):
        qs = self.banner_set.all().published()
        if self.random:
            qs = qs.order_by('?')
        else:
            qs = qs.order_by('display_order')
        return qs

    class Meta:
        verbose_name = _('banner slot')
        verbose_name_plural = _('banner slots')

class BannerQuerySet(models.query.QuerySet):
    def published(self):
        return self.filter(is_published=True)

class Banner(models.Model, TranslatedObjectMixin):
    slot = models.ForeignKey(Slot)
    file = models.ForeignKey(File)
    is_published = models.BooleanField(default=False)
    destination = models.CharField(max_length=255, null=True, blank=True)
    ordering = models.IntegerField(default=0)

    objects = TranslatedObjectManager()

    def __unicode__(self):
        trans = None

        # This might be provided using a .extra() clause to avoid hundreds of extra queries:
        if hasattr(self, "preferred_translation"):
            trans = getattr(self, "preferred_translation", u"")
        else:
            try:
                trans = unicode(self.translation)
            except models.ObjectDoesNotExist:
                pass
            except AttributeError, e:
                pass

        if trans:
            return trans
        else:
            return self.file.__unicode__()

    def save(self, force_insert=False, force_update=False):
        if not self.ordering:
            self.ordering = self.slot.banner_set.all().count() + 1
        return super(Banner, self).save(force_insert,force_update)

    class Meta:
        verbose_name = _('banner')
        verbose_name_plural = _('banners')

class BannerTranslation(Translation(Banner)):
    """
    Translated banner name and description.
    """

    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('banner translation')
        verbose_name_plural = _('banner translations')

    def __unicode__(self):
        return self.name
