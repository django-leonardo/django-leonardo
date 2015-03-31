
from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from feincms.content.application.models import ApplicationContent
from feincms.content.medialibrary.models import MediaFileContent
from feincms.content.richtext.models import RichTextContent
from feincms.module.page.models import Page
from hrcms.module.blog import models
from hrcms.module.blog.widget import *
from hrcms.module.lang.widget import *
from hrcms.module.nav.widget import *
from hrcms.module.web.widget import *

FEINCMS_REVERSE_MONKEY_PATCH = False

FEINCMS_FRONTEND_EDITING = True

PAGE_EXTENSIONS = [
    'feincms.module.extensions.datepublisher',
    'feincms.module.extensions.translations',
    'feincms.module.page.extensions.relatedpages',
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
    DjangoTemplateWidget,
    PageTitleWidget,
    PageTitleWidget,
    TableWidget,
    FeedReaderWidget,
    UserLoginWidget,
    LanguageSelectorWidget,
    RichTextContent
]

NAVIGATION_CONTENT_TYPES = [
    TreeNavigationWidget,
    ContentNavigationWidget,
    ContextNavigationWidget,
    LinearNavigationWidget,
    BreadcrumbsWidget,
    SiteMapWidget,
    SiteSearchWidget
]

BLOG_CONTENT_TYPES = [
    BlogCategoriesWidget,
    RecentBlogPostsWidget
]
