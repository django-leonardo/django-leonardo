
import six
import horizon
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from leonardo.site import leonardo_admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import RedirectView, TemplateView
from feincms.module.page.sitemap import PageSitemap
from .base import leonardo
from horizon.decorators import require_perms  # noqa
from django.utils.module_loading import module_has_submodule  # noqa
from django.utils.importlib import import_module  # noqa


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

# load all urls
# support .urls file and urls_conf = 'elephantblog.urls' on default module
for app, mod in six.iteritems(leonardo.get_app_modules(settings.APPS)):
    if hasattr(mod, 'default'):
        if module_has_submodule(mod, 'urls'):
            urls_mod = import_module('.urls', mod.__name__)
            _urlpatterns = []
            if hasattr(urls_mod, 'urlpatterns'):
                _urlpatterns += urls_mod.urlpatterns
        else:
            urlpatterns_name = getattr(mod.default, ' urls_conf', None)
            if urlpatterns_name:
                _urlpatterns += patterns('',
                                         url(r'', include(urlpatterns_name)),
                                         )
        urlpatterns += _urlpatterns
        """
        # Require login if not public.
        if not getattr(mod.default, 'public', False):
            _decorate_urlconf(urlpatterns, require_auth)
        """

if 'oauth' in getattr(settings, 'APPS', []):
    # All Auth
    urlpatterns += patterns('',
                            url(r'^accounts/', include('allauth.urls')),
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
