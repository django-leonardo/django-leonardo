from __future__ import unicode_literals

import re
import sys

import types
from django.conf import settings
from django.core.urlresolvers import resolve, Resolver404
from django.http import (build_request_repr, HttpRequest, HttpResponse,
                         HttpResponseNotFound)
from django.template import Context, Template
from django.template.defaultfilters import force_escape, pprint
from django.utils import lru_cache, six, timezone
from django.utils.datastructures import MultiValueDict
from django.utils.encoding import force_bytes, smart_text
from django.utils.module_loading import import_string
from django.utils.translation import ugettext as _
from django.views.debug import default_urlconf, get_safe_settings
from django.template.loader import render_to_string


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
    except:
        feincms_page = None
        slug = None
    else:
        # nested path is not allowed for this time
        try:
            slug = request.path_info.split("/")[-2:-1][0]
        except KeyError:
            raise Exception("Nested path is not allowed !")

    c = Context({
        'urlconf': urlconf,
        'root_urlconf': settings.ROOT_URLCONF,
        'request_path': error_url,
        'urlpatterns': tried,
        'reason': force_bytes(exception, errors='replace'),
        'request': request,
        'settings': get_safe_settings(),
        'raising_view_name': caller,
        'feincms_page': feincms_page,
        'slug': slug,
    })
    t = render_to_string(TECHNICAL_404_TEMPLATE, c)
    return HttpResponseNotFound(t, content_type='text/html')
