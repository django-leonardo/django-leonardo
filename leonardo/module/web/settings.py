
from __future__ import absolute_import

from feincms.content.application.models import ApplicationContent
from feincms.content.richtext.models import RichTextContent
from .widget import *

from .const import *
from .models import Page


FEINCMS_REVERSE_MONKEY_PATCH = False

FEINCMS_FRONTEND_EDITING = True

PAGE_EXTENSIONS = [
    'feincms.module.extensions.datepublisher',
    'feincms.module.extensions.translations',
    #'feincms.module.page.extensions.relatedpages',
    'feincms.module.page.extensions.navigation',
    'feincms.module.extensions.seo',
    'feincms.module.page.extensions.symlinks',
    'feincms.module.extensions.changedate',
]

APPLICATION_CHOICES = (
    ('hrcms.portal.device_catalog.urls', 'Robotice Device Catalog'),
    ('hrcms.module.auth.urls', 'API Auth', ),
    ('hrcms.module.eshop.urls', 'Eshop', ),
    ('hrcms.module.eshop.api.urls', 'Eshop API', ),
    ('elephantblog.urls', 'Blog'),
)

CONTENT_TYPES = [
    ApplicationContent,
    RichTextContent
]


Page.register_templates(*PAGE_TEMPLATES)
