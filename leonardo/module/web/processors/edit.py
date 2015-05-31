
from django.http import HttpResponseRedirect
from django.utils.cache import add_never_cache_headers


def frontendediting_request_processor(page, request):
    """
    Sets the frontend editing state in the cookie depending on the
    ``frontend_editing`` GET parameter and the user's permissions.
    """
    if 'frontend_editing' not in request.GET:
        return

    response = HttpResponseRedirect(request.path)

    if request.user.has_module_perms('page'):
        try:
            enable_fe = int(request.GET['frontend_editing']) > 0
        except ValueError:
            enable_fe = False

        if enable_fe:
            response.set_cookie(str('frontend_editing'), enable_fe)
        else:
            response.delete_cookie(str('frontend_editing'))

    # Redirect to cleanup URLs
    return response


def frontendediting_response_processor(page, request, response):
    # Add never cache headers in case frontend editing is active
    if (hasattr(request, 'COOKIES')
            and request.COOKIES.get('frontend_editing', False)):

        if hasattr(response, 'add_post_render_callback'):
            response.add_post_render_callback(add_never_cache_headers)
        else:
            add_never_cache_headers(response)
