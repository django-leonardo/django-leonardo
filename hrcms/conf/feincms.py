
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
"""
Page.register_extensions(
    'feincms.module.extensions.datepublisher',
    'feincms.module.extensions.translations',
    'feincms.module.page.extensions.relatedpages',
    'feincms.module.page.extensions.navigation',
    'feincms.module.extensions.seo',
    'feincms.module.page.extensions.symlinks',
    'feincms.module.extensions.changedate',
)
"""

PAGE_REGIONS = (
    ('main', _('Content')),
    ('sidebar', _('Sidebar'), 'inherited'),
    ('header', _('Header')),
    ('footer', _('Footer')),
    ('toolbar', _('Toolbar')),
    ('preview', _('Preview')),
    ('helper', _('Helper'))
)

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

#from hrcms.module.web.models import *

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

"""

Page.create_content_type(ApplicationContent, APPLICATIONS=APPLICATION_CHOICES)

# core web widgets
# Page.create_content_type(HtmlTextWidget) # not work something with
# translation
Page.create_content_type(DjangoTemplateWidget)
Page.create_content_type(PageTitleWidget)
Page.create_content_type(TableWidget)
Page.create_content_type(FeedReaderWidget)
Page.create_content_type(UserLoginWidget)

# language widgets
Page.create_content_type(LanguageSelectorWidget)

#multimedia widgets
Page.create_content_type(FlashObjectWidget)
Page.create_content_type(InternetVideoWidget)
Page.create_content_type(SimpleVideoWidget)
Page.create_content_type(DownloadListWidget)
Page.create_content_type(MediaGalleryWidget)
Page.create_content_type(SimpleImageWidget)
Page.create_content_type(VectorGraphicsWidget)
Page.create_content_type(AnnotatedImageWidget)
"""

"""
# navigation widgets
Page.create_content_type(TreeNavigationWidget)
Page.create_content_type(ContentNavigationWidget)
Page.create_content_type(ContextNavigationWidget)
Page.create_content_type(LinearNavigationWidget)
Page.create_content_type(BreadcrumbsWidget)
Page.create_content_type(SiteMapWidget)
Page.create_content_type(SiteSearchWidget)
"""

"""
# boardie
Page.create_content_type(PolarClockWidget)

Page.create_content_type(HorizonChartWidget)

Page.create_content_type(AreaChartWidget)

Page.create_content_type(SystemChartWidget)

Page.create_content_type(AngularGaugeWidget)
Page.create_content_type(ForceDirectedGraphWidget)
Page.create_content_type(ArcDiagramWidget)
"""

"""
Page.create_content_type(BlogCategoriesWidget)
Page.create_content_type(RecentBlogPostsWidget)

Page.register_with_reversion()
"""
