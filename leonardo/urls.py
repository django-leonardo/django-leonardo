
import horizon
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from leonardo.site import leonardo_admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import RedirectView, TemplateView
from feincms.module.page.sitemap import PageSitemap

from horizon.decorators import require_perms  # noqa

def _decorate_urlconf(urlpatterns, decorator, *args, **kwargs):
    for pattern in urlpatterns:
        if getattr(pattern, 'callback', None):
            pattern._callback = decorator(pattern.callback, *args, **kwargs)
        if getattr(pattern, 'url_patterns', []):
            _decorate_urlconf(pattern.url_patterns, decorator, *args, **kwargs)


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

if 'oauth' in getattr(settings, 'APPS', []):
    # All Auth
    urlpatterns += patterns('',
                            url(r'^accounts/', include('allauth.urls')),
                            )

if 'blog' in getattr(settings, 'APPS', []):
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
                        (r'^favicon\.ico$', RedirectView.as_view(
                            **{'url': '/static/img/favicon.ico'}),),
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

# for sentry error handler
if hasattr(settings, "ERROR_HANDLER_MODULE"):
    try:
        mod = __import__(getattr(settings, "ERROR_HANDLER_MODULE", None))
        handler500 = getattr(getattr(mod, "urls"), "handler500")
    except Exception, e:
        pass
