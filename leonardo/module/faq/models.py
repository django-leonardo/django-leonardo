# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext as __

from tinymce.models import HTMLField

from feincms.translations import TranslatedObjectMixin, Translation, TranslatedObjectManager

from webcms.utils.models import JSONField
from webcms.module.media.models import File

import logging
log = logging.getLogger('webcms.faq')

class FaqCategory(models.Model, TranslatedObjectMixin):
    objects = TranslatedObjectManager()

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
            return self.id

    class Meta:
        verbose_name = _('FAQ topic')
        verbose_name_plural = _('FAQ topics')


class FaqCategoryTranslation(Translation(FaqCategory)):
    """
    Translated category name and description.
    """

    name = models.CharField(_('name'), max_length=200)
    description = HTMLField(_('description'), blank=True)

    class Meta:
        verbose_name = _('text')
        verbose_name_plural = _('texts')

    def __unicode__(self):
        return self.name

class Faq(models.Model, TranslatedObjectMixin):
    category = models.ForeignKey(FaqCategory, verbose_name=_("category"))
    active = models.BooleanField(verbose_name=_("visible"), default=True)
    ordering = models.PositiveIntegerField(verbose_name=_("ordering"), default=0)

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
            return self.id

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')

class FaqTranslation(Translation(Faq)):
    """
    Translated question name and description.
    """

    question = models.CharField(_('question'), max_length=200)
    answer = HTMLField(_('answer'), blank=True)

    class Meta:
        verbose_name = _('text')
        verbose_name_plural = _('texts')

    def __unicode__(self):
        return self.question
