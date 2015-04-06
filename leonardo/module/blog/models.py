
from django.utils.translation import ugettext_lazy as _
from elephantblog.models import Entry
from feincms.content.medialibrary.models import MediaFileContent
from feincms.content.richtext.models import RichTextContent

Entry.register_extensions('feincms.module.extensions.datepublisher',
                          'feincms.module.extensions.translations',
                          )
Entry.register_regions(
    ('main', _('Main content area')),
)
Entry.create_content_type(RichTextContent, regions=('main',))
"""
Entry.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('default')),
))
"""
