
import horizon
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from leonardo.site import leonardo_admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import RedirectView, TemplateView
from feincms.module.page.sitemap import PageSitemap
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

                       url(r'^doc/', include('django.contrib.admindocs.urls')),
                       )

# admin
urlpatterns += patterns('',
                        url(r'^admin/', include(leonardo_admin.urls)),
                        url(r'^contrib/', include('horizon_contrib.urls'),),
                        )

# search
urlpatterns += patterns('',
                        #url(r'', include('haystack.urls')),
                        url(r'^select2/', include('django_select2.urls')),
                        )

# modules
if 'web' in getattr(settings, 'APPS', []):
    urlpatterns += patterns('',
                            url(r'', include('leonardo.module.web.urls')),
                                )

# All Auth
urlpatterns += patterns('',
                        url(r'^accounts/', include('allauth.urls')),
                        )

# Elephantblog urls
urlpatterns += patterns('',
                        url(r'^blog/', include('elephantblog.urls')),
                        )

# horizon and feinCMS
urlpatterns += patterns('',
                        url(r'', include(horizon.urls)),
                        url(r'', include('feincms.urls')),
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

sitemaps = {
    'pages': PageSitemap,
}

urlpatterns += patterns('',
                        (r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),
                        (r'^favicon\.ico$', RedirectView.as_view(),
                         {'url': '/media/theme/favicon.ico'}),
                        (r'^robots\.txt$',
                         TemplateView.as_view(template_name='robots.txt')),
                        (r'^crossdomain\.xml$',
                         TemplateView.as_view(template_name='crossdomain.xml')),
                        )

if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
