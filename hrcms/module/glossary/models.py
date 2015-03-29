# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext as __

from tinymce.models import HTMLField

from feincms.translations import TranslatedObjectMixin, Translation, TranslatedObjectManager

import logging
log = logging.getLogger('webcms.glossary')

class Term(models.Model, TranslatedObjectMixin):
    active = models.BooleanField(verbose_name=_("active"), default=True)
    synonym = models.ForeignKey('self', verbose_name=_("synonym"), blank=True, null=True)
    related = models.ManyToManyField('self', verbose_name=_("related terms"), blank=True, null=True)

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
        verbose_name = _('term')
        verbose_name_plural = _('terms')

class TermTranslation(Translation(Term)):
    """
    Translated term name and description.
    """
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(verbose_name=_("URI"))
    excerpt = HTMLField(_('excerpt'), blank=True)
    description = HTMLField(_('description'), blank=True)
    more = HTMLField(_('more information'), blank=True)
    wiki = models.URLField(verbose_name=_("wiki"), blank=True, null=True)

    class Meta:
        verbose_name = _('translation')
        verbose_name_plural = _('translations')

    def __unicode__(self):
        return self.name
