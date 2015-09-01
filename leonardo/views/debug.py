from __future__ import unicode_literals

import re

import types
from django.conf import settings
from django.core.urlresolvers import Resolver404, resolve
from django.http import HttpResponseNotFound
from django.template import RequestContext, Template
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.views.debug import default_urlconf, get_safe_settings

HIDDEN_SETTINGS = re.compile('API|TOKEN|KEY|SECRET|PASS|SIGNATURE')

CLEANSED_SUBSTITUTE = '********************'

TECHNICAL_404_TEMPLATE = '404_technical.html'


def technical_404_response(request, exception):
    "Create a technical 404 error response. The exception should be the Http404."
    try:
        error_url = exception.args[0]['path']
    except (IndexError, TypeError, KeyError):
        error_url = request.path_info[1:]  # Trim leading slash

    try:
        tried = exception.args[0]['tried']
    except (IndexError, TypeError, KeyError):
        tried = []
    else:
        if (not tried                           # empty URLconf
            or (request.path == '/'
                and len(tried) == 1             # default URLconf
                and len(tried[0]) == 1
                and getattr(tried[0][0], 'app_name', '') == getattr(tried[0][0], 'namespace', '') == 'admin')):
            return default_urlconf(request)

    urlconf = getattr(request, 'urlconf', settings.ROOT_URLCONF)
    if isinstance(urlconf, types.ModuleType):
        urlconf = urlconf.__name__

    caller = ''
    try:
        resolver_match = resolve(request.path)
    except Resolver404:
        pass
    else:
        obj = resolver_match.func

        if hasattr(obj, '__name__'):
            caller = obj.__name__
        elif hasattr(obj, '__class__') and hasattr(obj.__class__, '__name__'):
            caller = obj.__class__.__name__

        if hasattr(obj, '__module__'):
            module = obj.__module__
            caller = '%s.%s' % (module, caller)

    try:
        from leonardo.module.web.models import Page
        feincms_page = Page.objects.for_request(request, best_match=True)
        template = feincms_page.theme.template
    except:
        feincms_page = None
        slug = None
        template = None
    else:
        # nested path is not allowed for this time
        try:
            slug = request.path_info.split("/")[-2:-1][0]
        except KeyError:
            raise Exception("Nested path is not allowed !")

    c = RequestContext(request, {
        'urlconf': urlconf,
        'root_urlconf': settings.ROOT_URLCONF,
        'request_path': error_url,
        'urlpatterns': tried,
        'reason': force_bytes(exception, errors='replace'),
        'request': request,
        'settings': get_safe_settings(),
        'raising_view_name': caller,
        'feincms_page': feincms_page,
        'template': template or 'base.html',
        'standalone': True,
        'slug': slug,
    })

    try:
        t = render_to_string('404_technical.html', c)
    except:
        from django.views.debug import TECHNICAL_404_TEMPLATE
        t = Template(TECHNICAL_404_TEMPLATE).render(c)
    return HttpResponseNotFound(t, content_type='text/html')
