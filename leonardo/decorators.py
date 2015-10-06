
"""
General-purpose decorators for use with Leonardo.
"""
from __future__ import absolute_import, unicode_literals

import functools

from django.utils.decorators import available_attrs  # noqa
from django.utils.translation import ugettext_lazy as _


def require_auth(view_func):
    """Performs user authentication check.

    Similar to Django's `login_required` decorator, except that this throws
    :exc:`~leonardo.exceptions.NotAuthenticated` exception if the user is not
    signed-in.
    """
    from leonardo.exceptions import NotAuthenticated  # noqa

    @functools.wraps(view_func, assigned=available_attrs(view_func))
    def dec(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        raise NotAuthenticated(_("Please log in to continue."))
    return dec


def _decorate_urlconf(urlpatterns, decorator, *args, **kwargs):
    '''Decorate all urlpatterns by specified decorator'''

    if isinstance(urlpatterns, (list, tuple)):

        for pattern in urlpatterns:
            if getattr(pattern, 'callback', None):
                pattern._callback = decorator(pattern.callback, *args, **kwargs)
            if getattr(pattern, 'url_patterns', []):
                _decorate_urlconf(
                    pattern.url_patterns, decorator, *args, **kwargs)
    else:
        if getattr(urlpatterns, 'callback', None):
            urlpatterns._callback = decorator(
                urlpatterns.callback, *args, **kwargs)
