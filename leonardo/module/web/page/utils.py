
from django.contrib.auth.models import AnonymousUser
from django.core.handlers.base import BaseHandler
from django.test import RequestFactory
from leonardo.module.web.processors.config import ContextConfig


def get_anonymous_request(leonardo_page):
    """returns inicialized request
    """

    request_factory = RequestFactory()
    request = request_factory.get(
        leonardo_page.get_absolute_url(), data={})
    request.feincms_page = request.leonardo_page = leonardo_page
    request.frontend_editing = False
    request.user = AnonymousUser()

    if not hasattr(request, '_feincms_extra_context'):
        request._feincms_extra_context = {}

    request.path = leonardo_page.get_absolute_url()
    request.frontend_editing = False

    leonardo_page.run_request_processors(request)

    request.LEONARDO_CONFIG = ContextConfig(request)

    handler = BaseHandler()
    handler.load_middleware()

    # Apply request middleware
    for middleware_method in handler._request_middleware:
        try:
            middleware_method(request)
        except:
            pass

    # call processors
    for fn in reversed(list(leonardo_page.request_processors.values())):
        fn(leonardo_page, request)

    return request
