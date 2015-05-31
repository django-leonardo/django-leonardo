"""

code from https://github.com/TyMaszWeb/django-template-finder

"""
import fnmatch
import logging
import os
import re

from django.conf import settings
from django.utils.text import capfirst


try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module


try:
    from django.utils.six import string_types
except ImportError:
    string_types = (basestring,)
try:
    from django.template import Engine
except ImportError:
    class Engine(object):
        @staticmethod
        def get_default():
            return None


__all__ = ('find_all_templates', 'flatten_template_loaders', 'template_choices')


LOGGER = logging.getLogger('templatefinder')


def find_all_templates(pattern='*.html', ignore_private=True):
    """
    Finds all Django templates matching given glob in all TEMPLATE_LOADERS

    :param str pattern: `glob <http://docs.python.org/2/library/glob.html>`_
                        to match

    .. important:: At the moment egg loader is not supported.
    """
    templates = []
    template_loaders = flatten_template_loaders(settings.TEMPLATE_LOADERS)
    for loader_name in template_loaders:
        module, klass = loader_name.rsplit('.', 1)
        if loader_name in (
            'django.template.loaders.app_directories.Loader',
            'django.template.loaders.filesystem.Loader',
        ):
            loader_class = getattr(import_module(module), klass)
            if getattr(loader_class, '_accepts_engine_in_init', False):
                loader = loader_class(Engine.get_default())
            else:
                loader = loader_class()
            for dir in loader.get_template_sources(''):
                for root, dirnames, filenames in os.walk(dir):
                    for basename in filenames:
                        if ignore_private and basename.startswith("_"):
                            continue
                        filename = os.path.join(root, basename)
                        rel_filename = filename[len(dir)+1:]
                        if fnmatch.fnmatch(filename, pattern) or \
                           fnmatch.fnmatch(basename, pattern) or \
                           fnmatch.fnmatch(rel_filename, pattern):
                            templates.append(rel_filename)
        else:
            LOGGER.debug('%s is not supported' % loader_name)
    return sorted(set(templates))


def flatten_template_loaders(templates):
    """
    Given a collection of template loaders, unwrap them into one flat iterable.

    :param templates: template loaders to unwrap
    :return: template loaders as an iterable of strings.
    :rtype: generator expression
    """
    for loader in templates:
        if not isinstance(loader, string_types):
            for subloader in flatten_template_loaders(loader):
                yield subloader
        else:
            yield loader


def template_choices(templates, display_names=None, suffix=False):
    """
    Given an iterable of `templates`, calculate human-friendly display names
    for each of them, optionally using the `display_names` provided, or a
    global dictionary (`TEMPLATEFINDER_DISPLAY_NAMES`) stored in the Django
    project's settings.

    .. note:: As the resulting iterable is a lazy generator, if it needs to be
              consumed more than once, it should be turned into a `set`, `tuple`
              or `list`.

    :param list templates: an iterable of template paths, as returned by
                           `find_all_templates`
    :param display_names: If given, should be a dictionary where each key
                          represents a template path in `templates`, and each
                          value is the display text.
    :type display_names: dictionary or None
    :return: an iterable of two-tuples representing value (0) & display text (1)
    :rtype: generator expression
    """
    # allow for global template names, as well as usage-local ones.
    if display_names is None:
        display_names = getattr(settings, 'TEMPLATEFINDER_DISPLAY_NAMES', {})

    to_space_re = re.compile(r'[^a-zA-Z0-9\-]+')

    def fix_display_title(template_path):
        if template_path in display_names:
            return display_names[template_path]
        # take the last part from the template path; works even if there is no /
        lastpart = template_path.rpartition('/')[-1]
        # take everything to the left of the rightmost . (the file extension)
        if suffix:
            lastpart_with_suffix = lastpart
            return capfirst(lastpart_with_suffix)
        else:
            lastpart_minus_suffix = lastpart.rpartition('.')[0]
            # convert most non-alphanumeric characters into spaces, with the
            # exception of hyphens.
            lastpart_spaces = to_space_re.sub(' ', lastpart_minus_suffix)
        return capfirst(lastpart_spaces)

    return ((template, fix_display_title(template)) for template in templates)