# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models

from django.utils.translation import ugettext_lazy as _

from feincms.module.page.extensions.navigation import NavigationExtension, PagePretender
from feincms.content.application.models import reverse

from feincms.translations import TranslatedObjectMixin, Translation, TranslatedObjectManager
from mptt.models import MPTTModel

from webcms.module.media.models import Category as MediaCategory, File

from tinymce.models import HTMLField


class Category(MPTTModel, TranslatedObjectMixin):
    """
    An encapsulation of a portfolio category.
    """
    ordering = models.SmallIntegerField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    logo = models.ForeignKey(File, blank=True, null=True, verbose_name=_("logo"))
    active = models.BooleanField(default=True)

    objects = TranslatedObjectManager()

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['ordering',]

    class Meta:
        ordering = ('ordering',)
        verbose_name = _('portfolio category')
        verbose_name_plural = _('portfolio categories')
        unique_together = (("ordering", "parent"),)

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

class CategoryTranslation(Translation(Category)):
    """
    Translations for category.
    """
    title = models.CharField(max_length=255, verbose_name=_("title"))
    slug = models.SlugField(_('slug'),)
    summary = models.CharField(_('summary'), max_length=250, blank=True)
    description = HTMLField(_('description'), blank=True, null=True)

    class Meta:
        verbose_name = _('category text')
        verbose_name_plural = _('category texts')

    def __unicode__(self):
        return self.title

class Service(models.Model, TranslatedObjectMixin):
    """
    An encapsulation of a service.
    """
    ordering = models.IntegerField(blank=True, null=True)
    logo = models.ForeignKey(File, blank=True, null=True, verbose_name=_("logo"))
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('ordering',)
        verbose_name = _('service')
        verbose_name_plural = _('services')

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
            return u"[ no name ]"

class ServiceTranslation(Translation(Service)):
    """
    Translations for service.
    """
    title = models.CharField(max_length=255, verbose_name=_("title"))
    slug = models.SlugField(_('slug'),)
    summary = models.CharField(_('summary'), max_length=250, blank=True)
    description = HTMLField(_('description'), blank=True, null=True)

    class Meta:
        verbose_name = _('service translation')
        verbose_name_plural = _('service translations')

    def __unicode__(self):
        return self.title

class Client(models.Model, TranslatedObjectMixin):
    """
    A project's client.
    """
    logo = models.ForeignKey(File, blank=True, null=True, verbose_name=_("logo"))
    ordering = models.IntegerField(blank=True, null=True, verbose_name=_("ordering"))
    active = models.BooleanField(default=True, verbose_name=_("active"))

    class Meta:
        ordering = ('ordering',)
        verbose_name = _('client')
        verbose_name_plural = _('clients')

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
            return u"[ no name ]"

class ClientTranslation(Translation(Client)):
    """
    Translations for client.
    """
    title = models.CharField(max_length=255, verbose_name=_("title"))
    slug = models.SlugField(_('slug'),)
    summary = models.CharField(_('summary'), max_length=250, blank=True)
    description = HTMLField(_('description'), blank=True, null=True)

    class Meta:
        verbose_name = _('client translation')
        verbose_name_plural = _('client translations')

    def __unicode__(self):
        return self.title

class Project(models.Model, TranslatedObjectMixin):
    """
    An encapsualtion of a project.
    """
    categories = models.ManyToManyField(Category, verbose_name=_("categories"))
    client = models.ForeignKey(Client, verbose_name=_("client"), blank=True, null=True)
    files = models.ManyToManyField(File, blank=True, null=True, verbose_name=_("files"), through='ProjectFile')
    media_category = models.ForeignKey(MediaCategory, blank=True, null=True, verbose_name=_("media category"))
    services = models.ManyToManyField(Service, blank=True, null=True, verbose_name=_("services"))
    created = models.DateField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    objects = TranslatedObjectManager()

    class Meta:
        ordering = ('-created',)
        verbose_name = _('project')
        verbose_name_plural = _('projects')

    def get_main_file(self):
        qs = ProjectFile.objects.filter(featured=True, project=self)
        if qs.count() > 0:
            return qs[0]
        else:
            return None

    def get_other_files(self):
        qs = self.files.all()
        if qs.count() > 1:
            return qs[1:qs.count()]
        else:
            return None

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

class ProjectTranslation(Translation(Project)):
    """
    Translations for project.
    """
    title = models.CharField(max_length=255, verbose_name=_("title"))
    slug = models.SlugField(_('slug'),)
    summary = models.CharField(_('summary'), max_length=250, blank=True)
    description = HTMLField(_('description'), blank=True, null=True)

    class Meta:
        verbose_name = _('project text')
        verbose_name_plural = _('project texts')

    def __unicode__(self):
        return self.title

VALIDATION_CHOICES = (
    ('webcms.utils.validation.simple', _('One or more characters')),
    ('webcms.utils.validation.integer', _('Integer number')),
    ('webcms.utils.validation.yesno', _('Yes or No')),
    ('webcms.utils.validation.decimal', _('Decimal number')),
)

class AttributeOption(models.Model, TranslatedObjectMixin):
    """
    Allows arbitrary name/value pairs to be attached to a project.
    """
    ordering = models.IntegerField(_("sort order"), default=1)
    validation = models.CharField(_("field validations"), choices=VALIDATION_CHOICES, max_length=100)
    error_message = models.CharField(_("error message"), default=_("Invalid entry"), max_length=100)

    objects = TranslatedObjectManager()

    class Meta:
        ordering = ('ordering',)
        verbose_name = _('attribute option')
        verbose_name_plural = _('attribute options')

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

class AttributeOptionTranslation(Translation(AttributeOption)):
    """
    Translations for attribute option.
    """
    title = models.CharField(max_length=255, verbose_name=_("title"))
    summary = models.CharField(_('summary'), max_length=250, blank=True)

    class Meta:
        verbose_name = _('attribute option translation')
        verbose_name_plural = _('attribute option translations')

    def __unicode__(self):
        return self.title

class ProjectAttribute(models.Model):
    """
    Allows arbitrary name/value pairs (as strings) to be attached to a project.
    """
    project = models.ForeignKey(Project)
    languagecode = models.CharField(_('language'), max_length=10, choices=settings.LANGUAGES, null=True, blank=True)
    option = models.ForeignKey(AttributeOption)
    value = models.CharField(_("Value"), max_length=255)

    def _name(self):
        return self.option.name
    name = property(_name)

    def _description(self):
        return self.option.description
    description = property(_description)

    class Meta:
        verbose_name = _("Project attribute")
        verbose_name_plural = _("Project attributes")
        ordering = ('option__ordering',)

    def __unicode__(self):
        return self.option.name

class ProjectFile(models.Model):
    """
    Allows media files to be attached to a project.
    """
    project = models.ForeignKey(Project)
    file = models.ForeignKey(File)
    ordering = models.IntegerField(blank=True, null=True, verbose_name=_("ordering"))
    active = models.BooleanField(default=True, verbose_name=_("active"))
    featured = models.BooleanField(default=True, verbose_name=_("featured"))

    class Meta:
        verbose_name = _("Project file")
        verbose_name_plural = _("Project files")

    def __unicode__(self):
        return self.file.__unicode__()

class ProjectCategoriesNavigationExtension(NavigationExtension):
    name = _('All portfolio categories')

    def children(self, page, **kwargs):
        result = []
        base_url = page.get_absolute_url()
        for category in Category.objects.filter(active=True):
            result.append(PagePretender(
                title=category.__unicode__(),
                url= '%s%s/' % (base_url, category.translation.slug),
#                children=[]
            ))
        return result
