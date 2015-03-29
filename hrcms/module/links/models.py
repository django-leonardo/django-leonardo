# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields.json import JSONField
from feincms.translations import (TranslatedObjectManager,
                                  TranslatedObjectMixin, Translation)
from hrcms.module.media.models import File


class LinkCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name"))
    slug = models.CharField(max_length=255, verbose_name=_("slug"), blank=True)
    description = models.TextField(blank=True, verbose_name=_("description"))

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('link category')
        verbose_name_plural = _('link categories')


TARGET_CHOICES = (
    ('_none', _('same window')),
    ('_modal', _('modal window')),
    ('_blank', _('new tab')),
)


class Link(models.Model, TranslatedObjectMixin):
    web_address = models.CharField(
        max_length=255, verbose_name=_("web address"))
    target = models.CharField(max_length=255, verbose_name=_(
        "target"), choices=TARGET_CHOICES, default='_none')
    relationship = JSONField(
        blank=True, verbose_name=_("link relationship"), editable=False)
    image = models.ForeignKey(
        File, blank=True, null=True, verbose_name=_("image"))
    category = models.ForeignKey(LinkCategory, verbose_name=_("link category"))
    visible = models.BooleanField(verbose_name=_("visible"), default=True)
    ordering = models.PositiveIntegerField(
        verbose_name=_("ordering"), default=0)

    objects = TranslatedObjectManager()

    def __unicode__(self):
        trans = None

        # This might be provided using a .extra() clause to avoid hundreds of
        # extra queries:
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
            return self.web_address

    class Meta:
        ordering = ['ordering', ]
        verbose_name = _('link')
        verbose_name_plural = _('links')


class LinkTranslation(Translation(Link)):

    """
    Translated link name and description.
    """

    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('link translation')
        verbose_name_plural = _('link translations')

    def __unicode__(self):
        return self.name
