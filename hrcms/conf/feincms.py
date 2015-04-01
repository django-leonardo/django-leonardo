
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


PAGE_REGIONS = (
    ('main', _('Content')),
    ('sidebar', _('Sidebar'), 'inherited'),
    ('header', _('Header')),
    ('footer', _('Footer')),
    ('toolbar', _('Toolbar')),
    ('preview', _('Preview')),
    ('helper', _('Helper'))
)

#from hrcms.module.web.const import *

PAGE_TEMPLATES = (
    {
        'title': _('Page'),
        'key': 'page',
        'path': 'layout/page.html',
        'regions': PAGE_REGIONS,
    },
    {
        'title': _('Dashboard'),
        'key': 'dashboard',
        'path': 'layout/dashboard.html',
        'regions': PAGE_REGIONS,
    },
    {
        'title': _('API'),
        'key': 'api',
        'path': 'rest_framework/api.html',
        'regions': PAGE_REGIONS,
    },
)


Page.register_templates(*PAGE_TEMPLATES)

Page.create_content_type(RichTextContent)

APPLICATION_CHOICES = (
    #    ('webcms.module.web.apps.auth', _('User authentication')),
    #
    #    ('webcms.module.nav.apps.fulltext', _('Fulltext search')),
    #    ('webcms.module.nav.apps.googlesearch', _('Google search')),
    #
    #    ('webcms.module.glossary.apps.glossary', _('Glossary')),
    #
    #    ('webcms.module.media.apps.category_simple', _('Media categories')),
    #
    #    ('webcms.module.news.apps.news_archive', _('News archive')),
    #
    #    ('webcms.module.store.apps.core', _('Store (core application)')),
    #    ('webcms.module.store.apps.accounts', _('Store (user profile)')),
    #    ('webcms.module.store.apps.wishlist', _('Store (wishlist)')),
    #    ('webcms.module.store.apps.auth', _('Store (authentication)')),
    #    ('webcms.module.store.apps.registration', _('Store (registration)')),
    #    ('webcms.module.store.apps.category', _('Store (categories)')),
    #    ('webcms.module.store.apps.brand', _('Store (brands)')),
    #    ('webcms.module.store.apps.products', _('Store (products)')),
    #    ('webcms.module.store.apps.cart', _('Store (shopping cart)')),
    #    ('webcms.module.store.apps.payment', _('Store (payment process)')),
    #    ('webcms.module.store.apps.feeds', _('Store (feed exports)')),
    #    ('webcms.module.store.apps.branches', _('Store (branches)')),
    #
    #    ('webcms.module.folio.apps.category', _('Portfolio (by category)')),
    #    ('webcms.module.folio.apps.service', _('Portfolio (by service)')),

    ('hrcms.portal.device_catalog.urls', 'Robotice Device Catalog'),
    ('hrcms.module.auth.urls', 'API Auth', ),
    ('hrcms.module.eshop.urls', 'Eshop', ),
    ('hrcms.module.eshop.api.urls', 'Eshop API', ),
    ('elephantblog.urls', 'Blog'),
)

Page.register_with_reversion()
