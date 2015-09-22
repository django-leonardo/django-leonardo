
from django.utils import six
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.utils.importlib import import_module  # noqa
from django.utils.module_loading import module_has_submodule  # noqa
from django.views.generic.base import RedirectView, TemplateView
from feincms.module.page.sitemap import PageSitemap
from leonardo.site import leonardo_admin

from .base import leonardo
from leonardo.utils.settings import is_leonardo_module, get_conf_from_module
from .decorators import require_auth

__all__ = ['handler400', 'handler403', 'handler404', 'handler500']


def _decorate_urlconf(urlpatterns, decorator, *args, **kwargs):

    if isinstance(urlpatterns, (list, tuple)):

        for pattern in urlpatterns:
            if getattr(pattern, 'callback', None):
                pattern._callback = decorator(pattern.callback, *args, **kwargs)
            if getattr(pattern, 'url_patterns', []):
                _decorate_urlconf(pattern.url_patterns, decorator, *args, **kwargs)
    else:
        if getattr(urlpatterns, 'callback', None):
            urlpatterns._callback = decorator(urlpatterns.callback, *args, **kwargs)


urlpatterns = patterns('',
                       url(r'^contrib/', include('horizon_contrib.urls'),),
                       url(r'^select2/', include('django_select2.urls')),
                       )

# load all urls
# support .urls file and urls_conf = 'elephantblog.urls' on default module
# decorate all url patterns if is not explicitly excluded
for mod in getattr(settings, '_APPS', leonardo.get_app_modules(settings.APPS)):
    # TODO this not work
    if is_leonardo_module(mod):

        conf = get_conf_from_module(mod)

        if module_has_submodule(mod, 'urls'):
            urls_mod = import_module('.urls', mod.__name__)
            _urlpatterns = []
            if hasattr(urls_mod, 'urlpatterns'):
                # if not public decorate all

                if conf['public']:
                    urlpatterns += urls_mod.urlpatterns
                else:
                    _decorate_urlconf(urls_mod.urlpatterns,
                                      require_auth)
                    urlpatterns += urls_mod.urlpatterns

for urls_conf, conf in six.iteritems(getattr(settings, 'MODULE_URLS', {})):
    # is public ?
    try:
        if conf['is_public']:
            urlpatterns += \
                patterns('',
                         url(r'', include(urls_conf)),
                         )
        else:
            _decorate_urlconf(
                url(r'', include(urls_conf)),
                require_auth)
            urlpatterns += patterns('',
                                    url(r'', include(urls_conf)))
    except Exception as e:
        raise Exception('raised %s during loading %s' % (str(e), urls_conf))

if getattr(settings, 'LEONARDO_AUTH', True):
    urlpatterns += patterns('',
                            url(r'^auth/',
                                include('leonardo.module.leonardo_auth.auth_urls')),
                            )

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

if settings.DEBUG:

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

# feinCMS
urlpatterns += patterns('',
                        url(r'', include('feincms.urls')),
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

handler400 = getattr(settings, "HANDLER_400", 'leonardo.views.defaults.bad_request')
handler403 = getattr(settings, "HANDLER_403", 'leonardo.views.defaults.permission_denied')
handler404 = getattr(settings, "HANDLER_404", 'leonardo.views.defaults.page_not_found')
handler500 = getattr(settings, "HANDLER_500", 'leonardo.views.defaults.server_error')
