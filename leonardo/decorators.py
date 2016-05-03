
"""
General-purpose decorators for use with Leonardo.
"""
from __future__ import absolute_import, unicode_literals

import functools
import sys

from django.utils.decorators import available_attrs  # noqa
from django.utils.translation import ugettext_lazy as _

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


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


def staff_member(view_func):
    """Performs user authentication check.

    Similar to Django's `login_required` decorator, except that this throws
    :exc:`~leonardo.exceptions.NotAuthenticated` exception if the user is not
    signed-in.
    """
    from leonardo.exceptions import NotAuthorized  # noqa

    @functools.wraps(view_func, assigned=available_attrs(view_func))
    def dec(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        raise NotAuthorized(_("You haven't permissions to do this action."))
    return dec


def _decorate_urlconf(urlpatterns, decorator=require_auth, *args, **kwargs):
    '''Decorate all urlpatterns by specified decorator'''

    if isinstance(urlpatterns, (list, tuple)):

        for pattern in urlpatterns:
            if getattr(pattern, 'callback', None):
                pattern._callback = decorator(
                    pattern.callback, *args, **kwargs)
            if getattr(pattern, 'url_patterns', []):
                _decorate_urlconf(
                    pattern.url_patterns, decorator, *args, **kwargs)
    else:
        if getattr(urlpatterns, 'callback', None):
            urlpatterns._callback = decorator(
                urlpatterns.callback, *args, **kwargs)

# make this method public
decorate_urlconf = _decorate_urlconf


def catch_result(task_func):
    """Catch printed result from Celery Task and return it in task response
    """

    @functools.wraps(task_func, assigned=available_attrs(task_func))
    def dec(*args, **kwargs):
        # inicialize
        orig_stdout = sys.stdout
        sys.stdout = content = StringIO()
        task_response = task_func(*args, **kwargs)
        # catch
        sys.stdout = orig_stdout
        content.seek(0)
        # propagate to the response
        task_response['stdout'] = content.read()
        return task_response
    return dec
