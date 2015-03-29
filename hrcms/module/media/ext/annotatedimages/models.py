# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.utils import translation
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from feincms.translations import TranslatedObjectMixin, Translation, TranslatedObjectManager
from tinymce.models import HTMLField 

from webcms.module.media.models import File

class AnnotatedImage(models.Model):
    image = models.ForeignKey(File, verbose_name=_("image"), limit_choices_to={'type': 'image'})

    class Meta:
        verbose_name = _("annotated image")
        verbose_name_plural = _('annotated images')

    def __unicode__(self):
        return u'%s (%s)' % (self.image.__unicode__(), self.id)

TOOLTIP_POSITION_CHOICES = (
    ('top', _('above')),
    ('bottom', _('below')),
    ('left', _('to left')),
    ('right', _('to right')),
)

class ImageAnnotation(models.Model, TranslatedObjectMixin):
    image = models.ForeignKey(AnnotatedImage, verbose_name=_("image"), related_name='annotations')
    number = models.IntegerField(max_length=255, verbose_name=_("number"), blank=True, null=True)
    position = models.CharField(max_length=255, verbose_name=_("position"), default='top', choices=TOOLTIP_POSITION_CHOICES)
    link = models.CharField(max_length=255, verbose_name=_("link"), blank=True, null=True)
    date = models.DateTimeField(verbose_name=_("date"), default=datetime.now())
    active = models.BooleanField(verbose_name=_("active"), blank=True)
    left = models.DecimalField(verbose_name=_("left"), decimal_places=3, max_digits=5)
    top = models.DecimalField(verbose_name=_("top"), decimal_places=3, max_digits=5)
    width = models.DecimalField(verbose_name=_("width"), decimal_places=3, max_digits=5)
    height = models.DecimalField(verbose_name=_("height"), decimal_places=3, max_digits=5)
    author = models.ForeignKey(User, verbose_name=_("author"), blank=True, null=True)
    objects = TranslatedObjectManager()

    class Meta:
        verbose_name = _("image annotation")
        verbose_name_plural = _('image annotations')

    def __unicode__(self):
        trans = None

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
            return u"[ no name ]"

class ImageAnnotationTranslation(Translation(ImageAnnotation)):
    """
    Translations for category.
    """
    title = models.CharField(max_length=255, verbose_name=_("title"), blank=True, null=True)
    description = HTMLField(verbose_name=_("description"), blank=True, null=True)

    class Meta:
        verbose_name = _('annotation text')
        verbose_name_plural = _('annotation texts')

    def __unicode__(self):
        return self.title
