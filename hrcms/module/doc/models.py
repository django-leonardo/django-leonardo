from datetime import datetime

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _

from feincms.admin import editor
from feincms.management.checker import check_database_schema
from feincms.models import Base
from feincms.utils import get_object

from tinymce.models import HTMLField
from webcms.utils.models import MultiSelectField
from webcms.module.business.models import Entity

content = ('content', _('Document content'))
front = ('front', _('Front page'))
preview = ('preview', _('Content preview'))

DOCUMENT_TEMPLATES = (
{
    'title': _('Document layout'),
    'key': 'doc',
    'path': 'layout/document.html',
    'regions': (content, front, preview,),
},
)

DOCUMENT_REGIONS = (
    ('content', _('Document content')),
    ('front', _('Front page')),
    ('preview', _('Content preview')),
)

DOCUMENT_OUTPUTS = (
    ('html', _('Web page (HTML)')),
    ('eml', _('E-mail message (HTML)')),
    ('rml', _('Print format (PDF)')),
    ('odt', _('Print format (ODT)')),
)

class DocumentManager(models.Manager):
    def published(self):
        return self.filter(
            published__isnull=False,
            published_on__lte=datetime.now(),
        )

class Document(Base):
    title = models.CharField(_('title'), max_length=255)
    language = models.CharField(_('language'), max_length=10, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE)
    outputs = MultiSelectField(max_length=255, verbose_name=_('outputs'), choices=DOCUMENT_OUTPUTS)
    supplier = models.ForeignKey(Entity, verbose_name=_('supplier'), related_name='doc_supplier')
    client = models.ForeignKey(Entity, verbose_name=_('client'), related_name='doc_client')
    summary = HTMLField(_('description'), blank=True, null=True)
    published = models.BooleanField(_('published'), default=False)
    published_on = models.DateTimeField(_('published on'), blank=True, null=True,
        help_text=_('Will be set automatically once you set the `published` above.'))
    author = models.ForeignKey(User, verbose_name=_('author'), blank=True, null=True)

    class Meta:
        get_latest_by = 'published_on'
        ordering = ['-published_on']
        verbose_name = _('document')
        verbose_name_plural = _('documents')

    objects = DocumentManager()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.published and not self.published_on:
            self.published_on = datetime.now()
        super(Document, self).save(*args, **kwargs)

#    @models.permalink
#    def get_absolute_url(self):
#        return ('blog_entry_detail', (self.id,), {})

    def get_url(self):
        return '%s/' % self.id

    @classmethod
    def register_extension(cls, register_fn):
        register_fn(cls, DocumentAdmin)

class DocumentAdmin(editor.ItemEditor):
    date_hierarchy = 'published_on'
    list_display = ('__unicode__', 'author', 'published', 'published_on', 'language')
    list_filter = ('published', 'author')
    search_fields = ('title', 'summary',)
    raw_id_fields = []

signals.post_syncdb.connect(check_database_schema(Document, __name__), weak=False)
