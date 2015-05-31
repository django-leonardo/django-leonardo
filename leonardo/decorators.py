
"""
General-purpose decorators for use with Leonardo.
"""
from __future__ import absolute_import, unicode_literals

import functools
from functools import wraps

from django.http import HttpResponse
from django.template.response import TemplateResponse
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


def standalone(view_func):
    """
    Marks the view method as standalone view; this means that
    ``HttpResponse`` objects returned from ``ApplicationContent``
    are returned directly, without further processing.
    """

    def inner(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        if isinstance(response, HttpResponse):
            response.context_data['standalone'] = True
            # support for feincms tags
            response.standalone = True
        return response
    return wraps(view_func)(inner)
