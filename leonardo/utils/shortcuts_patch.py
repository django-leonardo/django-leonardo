
import warnings

import django
from django.http import HttpResponse
from django.template import RequestContext, loader

if django.VERSION < (1, 9):

    from django.utils.deprecation import RemovedInDjango110Warning
    from django.template.context import _current_app_undefined
    from django.template.engine import (_context_instance_undefined,
                                        _dictionary_undefined, _dirs_undefined)

    def render(request, template_name, context={},
               context_instance=_context_instance_undefined,
               content_type=None, status=None, current_app=_current_app_undefined,
               dirs=_dirs_undefined, dictionary=_dictionary_undefined,
               using=None):
        """
        Returns a HttpResponse whose content is filled with the result of calling
        django.template.loader.render_to_string() with the passed arguments.
        """

        if hasattr(request, '_feincms_extra_context') and 'widget' in request._feincms_extra_context:
            context['widget'] = request._feincms_extra_context['widget']

        if (context_instance is _context_instance_undefined
                and current_app is _current_app_undefined
                and dirs is _dirs_undefined
                and dictionary is _dictionary_undefined):
            # No deprecated arguments were passed - use the new code path
            # In Django 1.10, request should become a positional argument.
            content = loader.render_to_string(
                template_name, context, request=request, using=using)

        else:
            # Some deprecated arguments were passed - use the legacy code path
            if context_instance is not _context_instance_undefined:
                if current_app is not _current_app_undefined:
                    raise ValueError('If you provide a context_instance you must '
                                     'set its current_app before calling render()')
            else:
                context_instance = RequestContext(request)
                if current_app is not _current_app_undefined:
                    warnings.warn(
                        "The current_app argument of render is deprecated. "
                        "Set the current_app attribute of request instead.",
                        RemovedInDjango110Warning, stacklevel=2)
                    request.current_app = current_app
                    # Directly set the private attribute to avoid triggering the
                    # warning in RequestContext.__init__.
                    context_instance._current_app = current_app

            content = loader.render_to_string(
                template_name, context, context_instance, dirs, dictionary,
                using=using)

        return HttpResponse(content, content_type, status)

else:

    def render(request, template_name, context={}, content_type=None, status=None, using=None):
        """
        Returns a HttpResponse whose content is filled with the result of calling
        django.template.loader.render_to_string() with the passed arguments.
        """

        if hasattr(request, '_feincms_extra_context') and 'widget' in request._feincms_extra_context:
            context['widget'] = request._feincms_extra_context['widget']
        content = loader.render_to_string(
            template_name, context, request, using=using)
        return HttpResponse(content, content_type, status)


def patch_shortcuts():

    django.shortcuts.render = render
