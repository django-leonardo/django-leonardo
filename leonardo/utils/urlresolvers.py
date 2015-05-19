from __future__ import unicode_literals

import sys

from django.conf import settings
from django.template.base import Library
from django.utils import six
from django.utils.encoding import smart_text
from leonardo.module.web.widget import ApplicationWidget
from leonardo.module.web.widget.application.reverse import app_reverse as do_app_reverse

register = Library()


def render(self, context):
    from django.core.urlresolvers import reverse, NoReverseMatch
    args = [arg.resolve(context) for arg in self.args]
    kwargs = {
        smart_text(k, 'ascii'): v.resolve(context)
        for k, v in self.kwargs.items()
    }

    view_name = self.view_name.resolve(context)

    try:
        current_app = context.request.current_app
    except AttributeError:
        # Change the fallback value to None when the deprecation path for
        # Context.current_app completes in Django 2.0.
        current_app = context.current_app

    # Try to look up the URL twice: once given the view name, and again
    # relative to what we guess is the "main" app. If they both fail,
    # re-raise the NoReverseMatch unless we're using the
    # {% url ... as var %} construct in which case return nothing.
    url = ''

    try:
        url = reverse(
            view_name, args=args, kwargs=kwargs, current_app=current_app)
    except NoReverseMatch:
        # try external apps
        for urlconf, config in six.iteritems(
                ApplicationWidget._feincms_content_models[0].ALL_APPS_CONFIG):
            partials = view_name.split(':')[1:]
            try:
                url = do_app_reverse(
                    ':'.join(partials), urlconf, args=args, kwargs=kwargs,
                    current_app=context.current_app)
            except NoReverseMatch:
                pass
            else:
                return url

        exc_info = sys.exc_info()
        if settings.SETTINGS_MODULE:
            project_name = settings.SETTINGS_MODULE.split('.')[0]
            try:
                url = reverse(project_name + '.' + view_name,
                              args=args, kwargs=kwargs,
                              current_app=current_app)
            except NoReverseMatch:
                if self.asvar is None:
                    # Re-raise the original exception, not the one with
                    # the path relative to the project. This makes a
                    # better error message.
                    six.reraise(*exc_info)
        else:
            if self.asvar is None:
                raise

    if self.asvar:
        context[self.asvar] = url
        return ''
    else:
        return url
