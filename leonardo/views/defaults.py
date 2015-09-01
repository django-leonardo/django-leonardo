
from django import http
from django.template import (Context, RequestContext,
                             loader, Template, TemplateDoesNotExist)
from django.views.decorators.csrf import requires_csrf_token
from django.template.loader import render_to_string

CONTENT_TYPE = 'text/html'


def _get_page_from_request(request):
    """return page from request
    """

    try:
        from leonardo.module.web.models import Page
        feincms_page = Page.objects.for_request(request, best_match=True)
    except:
        feincms_page = None

    return feincms_page


def render_in_page(request, template):

    """return rendered template in standalone mode or ``False``
    """

    page = _get_page_from_request(request)

    if page:
        try:
            slug = request.path_info.split("/")[-2:-1][0]
        except KeyError:
            slug = None

        body = render_to_string(template, RequestContext(request, {
            'request_path': request.path,
            'feincms_page': page,
            'slug': slug,
            'standalone': True}))
        return http.HttpResponseNotFound(body, content_type=CONTENT_TYPE)

    return False


# This can be called when CsrfViewMiddleware.process_view has not run,
# therefore need @requires_csrf_token in case the template needs
# {% csrf_token %}.
@requires_csrf_token
def page_not_found(request, template_name='404.html'):
    """
    Default 404 handler.

    Templates: :template:`404.html`
    Context:
        request_path
            The path of the requested URL (e.g., '/app/pages/bad_page/')
    """
    response = render_in_page(request, template_name)

    if response:
        return response

    template = Template(
        '<h1>Not Found</h1>'
        '<p>The requested URL {{ request_path }} was not found on this server.</p>')
    body = template.render(RequestContext(request, {'request_path': request.path}))
    return http.HttpResponseNotFound(body, content_type=CONTENT_TYPE)


@requires_csrf_token
def server_error(request, template_name='500.html'):
    """
    500 error handler.

    Templates: :template:`500.html`
    Context: None
    """

    response = render_in_page(request, template_name)

    if response:
        return response

    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return http.HttpResponseServerError('<h1>Server Error (500)</h1>', content_type='text/html')
    return http.HttpResponseServerError(template.render(Context({})))


@requires_csrf_token
def bad_request(request, template_name='400.html'):
    """
    400 error handler.

    Templates: :template:`400.html`
    Context: None
    """

    response = render_in_page(request, template_name)

    if response:
        return response

    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return http.HttpResponseBadRequest('<h1>Bad Request (400)</h1>', content_type='text/html')
    return http.HttpResponseBadRequest(template.render(Context({})))


# This can be called when CsrfViewMiddleware.process_view has not run,
# therefore need @requires_csrf_token in case the template needs
# {% csrf_token %}.
@requires_csrf_token
def permission_denied(request, template_name='403.html'):
    """
    Permission denied (403) handler.

    Templates: :template:`403.html`
    Context: None

    If the template does not exist, an Http403 response containing the text
    "403 Forbidden" (as per RFC 2616) will be returned.
    """

    response = render_in_page(request, template_name)

    if response:
        return response

    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return http.HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')
    return http.HttpResponseForbidden(template.render(RequestContext(request)))


def shortcut(request, content_type_id, object_id):
    from django.contrib.contenttypes.views import shortcut as real_shortcut
    return real_shortcut(request, content_type_id, object_id)
