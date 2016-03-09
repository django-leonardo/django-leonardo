
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import RedirectView, TemplateView
from feincms.module.page.sitemap import PageSitemap
from leonardo.views.page import Handler
from leonardo.views.select2 import Select2ResponseView
from constance import config
from .base import leonardo

__all__ = ['handler400', 'handler403', 'handler404', 'handler500']

urlpatterns = [
    url(r'^contrib/', include('horizon_contrib.urls'),),
    url(r"^fields/auto.json$",
        Select2ResponseView.as_view(), name="django_select2-json"),
]

if getattr(settings, 'LEONARDO_AUTH', True):
    urlpatterns += patterns('',
                            url(r'^auth/',
                                include('leonardo.module.leonardo_auth.auth_urls')),
                            )

urlpatterns += leonardo.urlpatterns

if getattr(settings, 'HORIZON_ENABLED', True):
    import horizon
    urlpatterns += patterns('',
                            url(r'', include(horizon.urls)),
                            )

# translation
urlpatterns += patterns('',
                        url(r'^i18n/js/(?P<packages>\S+?)/$',
                            'django.views.i18n.javascript_catalog',
                            name='jsi18n'),
                        url(r'^i18n/setlang/$',
                            'django.views.i18n.set_language',
                            name="set_language"),
                        url(r'^i18n/', include('django.conf.urls.i18n'))
                        )
# secure media
urlpatterns += patterns('',
                        url(r'^', include('leonardo.module.media.server.urls'))
                        )

if settings.DEBUG or getattr(settings, 'LEONARDO_SERVE_STATIC', False):

    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    try:
        import debug_toolbar
        urlpatterns += patterns('',
                                url(r'^__debug__/', include(debug_toolbar.urls)),
                                )
    except ImportError:
        pass


handler = Handler.as_view()

urlpatterns += patterns(
    '',
    url(r'^$', handler, name='feincms_home'),
    url(r'^(.*)/$', handler, name='feincms_handler'),
)

sitemaps = {
    'pages': PageSitemap,
}

if not settings.DEBUG or not getattr(settings, 'LEONARDO_PREVIEW', False):
    robots_template = 'robots.txt'
else:
    robots_template = 'robots_dev.txt'

urlpatterns += patterns('',
                        (r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),
                        (r'^favicon\.ico$', RedirectView.as_view(
                            **{'permanent': True, 'url': config.FAVICON_PATH}),),
                        (r'^robots\.txt$',
                         TemplateView.as_view(template_name=robots_template)),
                        (r'^crossdomain\.xml$',
                         TemplateView.as_view(template_name='crossdomain.xml')),
                        )

handler400 = getattr(settings, "HANDLER_400",
                     'leonardo.views.defaults.bad_request')
handler403 = getattr(settings, "HANDLER_403",
                     'leonardo.views.defaults.permission_denied')
handler404 = getattr(settings, "HANDLER_404",
                     'leonardo.views.defaults.page_not_found')
handler500 = getattr(settings, "HANDLER_500",
                     'leonardo.views.defaults.server_error')
