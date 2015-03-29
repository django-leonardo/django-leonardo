
from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from feincms.content.application.models import ApplicationContent
from feincms.content.medialibrary.models import MediaFileContent
from feincms.content.richtext.models import RichTextContent
from feincms.module.page.models import Page

from hrcms.module.lang.widget import *
from hrcms.module.nav.widget import *
from hrcms.module.web.widget import *

FEINCMS_REVERSE_MONKEY_PATCH = False

Page.register_extensions(
    'feincms.module.extensions.datepublisher',
    'feincms.module.extensions.translations',
    'feincms.module.page.extensions.relatedpages',
    'feincms.module.extensions.seo',
    'feincms.module.page.extensions.symlinks',
    'feincms.module.extensions.changedate'
)

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
        'title': _('Standard'),
        'key': 'base',
        'path': 'base.html',
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
Page.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('default')),
    ('lightbox', _('lightbox')),
))

Page.create_content_type(ApplicationContent, APPLICATIONS=(
    ('hrcms.portal.device_catalog.urls', 'Robotice Device Catalog'),
    ('hrcms.module.auth.urls', 'API Auth', ),
    ('hrcms.module.eshop.urls', 'Eshop', ),
    ('hrcms.module.eshop.api.urls', 'Eshop API', ),
))

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

"""

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

# navigation widgets
Page.create_content_type(TreeNavigationWidget)
Page.create_content_type(ContentNavigationWidget)
Page.create_content_type(ContextNavigationWidget)
Page.create_content_type(LinearNavigationWidget)
Page.create_content_type(BreadcrumbsWidget)
Page.create_content_type(SiteMapWidget)
Page.create_content_type(SiteSearchWidget)


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
