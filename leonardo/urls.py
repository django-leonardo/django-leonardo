
import six
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from leonardo.site import leonardo_admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import RedirectView, TemplateView
from feincms.module.page.sitemap import PageSitemap
from .base import leonardo
from django.utils.module_loading import module_has_submodule  # noqa
from django.utils.importlib import import_module  # noqa

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

# load all urls
# support .urls file and urls_conf = 'elephantblog.urls' on default module
# TODO: decorate loaded modules for sure
for app, mod in six.iteritems(leonardo.get_app_modules(settings.APPS)):
    if hasattr(mod, 'default'):
        if module_has_submodule(mod, 'urls'):
            urls_mod = import_module('.urls', mod.__name__)
            _urlpatterns = []
            if hasattr(urls_mod, 'urlpatterns'):
                urlpatterns += urls_mod.urlpatterns
        else:
            urlpatterns_name = getattr(mod.default, 'urls_conf', None)
            if urlpatterns_name:
                urlpatterns += \
                    patterns('',
                             url(r'', include(urlpatterns_name)),
                             )

if getattr(settings, 'LEONARDO_AUTH', True):
    urlpatterns += patterns('',
                            url(r'^auth/', include('leonardo.module.auth.urls')),
                            )

if getattr(settings, 'HORIZON_ENABLED', True):
    import horizon
    urlpatterns += patterns('',
                            url(r'', include(horizon.urls)),
                            )

if 'oauth' in getattr(settings, 'APPS', []):
    # All Auth
    urlpatterns += patterns('',
                            url(r'^accounts/', include('allauth.urls')),
                            )

# feinCMS
urlpatterns += patterns('',
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
                            **{'permanent': True, 'url': '/static/img/favicon.ico'}),),
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
