
from django.http import HttpResponseRedirect
from django.utils.cache import add_never_cache_headers
from django.core.cache import caches


WEBFONT_COOKIE_NAME = 'wfont'


def webfont_cookie(request):
    '''Adds WEBFONT Flag to the context'''

    if hasattr(request, 'COOKIES') and request.COOKIES.get(WEBFONT_COOKIE_NAME, None):

        return {
            WEBFONT_COOKIE_NAME.upper(): True
        }

    return {
        WEBFONT_COOKIE_NAME.upper(): False
    }
