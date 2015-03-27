
from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from feincms.content.application.models import ApplicationContent
from feincms.content.medialibrary.models import MediaFileContent
from feincms.content.richtext.models import RichTextContent
from feincms.module.page.models import Page

FEINCMS_REVERSE_MONKEY_PATCH = False

Page.register_extensions('feincms.module.page.extensions.navigation')

Page.register_extensions(
    'feincms.module.extensions.datepublisher',
    'feincms.module.extensions.translations',
    'feincms.module.page.extensions.navigation',
    'feincms.module.page.extensions.titles',
    'feincms.module.page.extensions.navigationgroups',
    'feincms.module.page.extensions.relatedpages',
    'feincms.module.extensions.seo',
    'feincms.module.page.extensions.symlinks',
    'feincms.module.extensions.featured',
    'feincms.module.page.extensions.excerpt',
    'feincms.module.extensions.changedate',
)

Page.register_templates({
    'title': _('Standard template'),
    'path': 'base.html',
    'regions': (
        ('main', _('Main content area')),
        ('sidebar', _('Sidebar'), 'inherited'),
    ),
})

Page.create_content_type(RichTextContent)
Page.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('default')),
    ('lightbox', _('lightbox')),
))

Page.create_content_type(ApplicationContent, APPLICATIONS=(
    ('hrcms.portal.device_catalog.urls', 'Horizon'),
    ('hrcms.module.auth.urls', 'API Auth', ),
    ))