from __future__ import unicode_literals, with_statement

import logging

from compressor.cache import cache_set
from compressor.conf import settings
from compressor.exceptions import CompressorError, FilterDoesNotExist
from compressor.filters import CachedCompilerFilter
from compressor.filters.css_default import CssAbsoluteFilter
from compressor.utils import get_mod_func
from django import template
from django.utils import six

try:
    from importlib import import_module
except:
    from django.utils.importlib import import_module

try:
    from urllib.request import url2pathname
except ImportError:
    from urllib import url2pathname

LOG = logging.getLogger(__name__)

# Some constants for nicer handling.
SOURCE_HUNK, SOURCE_FILE = 'inline', 'file'
METHOD_INPUT, METHOD_OUTPUT = 'input', 'output'

register = template.Library()

OUTPUT_FILE = 'file'
OUTPUT_INLINE = 'inline'
OUTPUT_MODES = (OUTPUT_FILE, OUTPUT_INLINE)


def compress_monkey_patch():
    """patch all compress

    we need access to variables from widget scss

    for example we have::

        /themes/bootswatch/cyborg/_variables

    but only if is cyborg active for this reasone we need
    dynamically append import to every scss file

    """
    from compressor.templatetags import compress as compress_tags
    from compressor import base as compress_base

    compress_base.Compressor.filter_input = filter_input
    compress_base.Compressor.output = output
    compress_base.Compressor.hunks = hunks
    compress_base.Compressor.precompile = precompile

    compress_tags.CompressorMixin.render_compressed = render_compressed

    from django_pyscss import compressor as pyscss_compressor

    pyscss_compressor.DjangoScssFilter.input = input


def render_compressed(self, context, kind, mode, forced=False):

    # See if it has been rendered offline
    if self.is_offline_compression_enabled(forced) and not forced:
        return self.render_offline(context)

    # Take a shortcut if we really don't have anything to do
    if (not settings.COMPRESS_ENABLED and
            not settings.COMPRESS_PRECOMPILERS and not forced):
        return self.get_original_content(context)

    context['compressed'] = {'name': getattr(self, 'name', None)}
    compressor = self.get_compressor(context, kind)

    # Check cache
    cache_key = None
    if settings.COMPRESS_ENABLED and not forced:
        cache_key, cache_content = self.render_cached(compressor, kind, mode)
        if cache_content is not None:
            return cache_content

    rendered_output = compressor.output(mode, forced=forced, context=context)

    assert isinstance(rendered_output, six.string_types)
    if cache_key:
        cache_set(cache_key, rendered_output)
    return rendered_output


def input(self, **kwargs):
    """main override which append variables import to all scss content
    """

    with_variables = None

    context = kwargs.get('context', {})

    try:
        context['leonardo_page']['theme']
        context['leonardo_page']['color_scheme']
    except Exception as e:
        LOG.exception(str(e))
    else:
        with_variables = """
        @import "/themes/{}/{}/_variables";
        {}
        """.format(
            context['leonardo_page']['theme']['name'],
            context['leonardo_page']['color_scheme']['name'],
            self.content)

    return self.compiler.compile_string(
        with_variables or self.content,
        filename=self.filename)


def hunks(self, forced=False, context=None):
    """
    The heart of content parsing, iterates over the
    list of split contents and looks at its kind
    to decide what to do with it. Should yield a
    bunch of precompiled and/or rendered hunks.
    """
    enabled = settings.COMPRESS_ENABLED or forced

    for kind, value, basename, elem in self.split_contents():
        precompiled = False
        attribs = self.parser.elem_attribs(elem)
        charset = attribs.get("charset", self.charset)
        options = {
            'method': METHOD_INPUT,
            'elem': elem,
            'kind': kind,
            'basename': basename,
            'charset': charset,
            'context': context
        }

        if kind == SOURCE_FILE:
            options = dict(options, filename=value)
            value = self.get_filecontent(value, charset)

        if self.precompiler_mimetypes:
            precompiled, value = self.precompile(value, **options)

        if enabled:
            yield self.filter(value, self.cached_filters, **options)
        elif precompiled:
            # since precompiling moves files around, it breaks url()
            # statements in css files. therefore we run the absolute filter
            # on precompiled css files even if compression is disabled.
            if CssAbsoluteFilter in self.cached_filters:
                value = self.filter(value, [CssAbsoluteFilter], **options)
            yield self.handle_output(kind, value, forced=True,
                                     basename=basename)
        else:
            yield self.parser.elem_str(elem)


def output(self, mode='file', forced=False, context=None):
    """
    The general output method, override in subclass if you need to do
    any custom modification. Calls other mode specific methods or simply
    returns the content directly.
    """
    output = '\n'.join(self.filter_input(forced, context=context))

    if not output:
        return ''

    if settings.COMPRESS_ENABLED or forced:
        filtered_output = self.filter_output(output)
        return self.handle_output(mode, filtered_output, forced)

    return output


def filter_input(self, forced=False, context=None):
    """
    Passes each hunk (file or code) to the 'input' methods
    of the compressor filters.
    """
    content = []
    for hunk in self.hunks(forced, context=context):
        content.append(hunk)
    return content


def precompile(self, content, kind=None, elem=None, filename=None,
               charset=None, **kwargs):
    """
    Processes file using a pre compiler.
    This is the place where files like coffee script are processed.
    """
    if not kind:
        return False, content
    attrs = self.parser.elem_attribs(elem)
    mimetype = attrs.get("type", None)
    if mimetype is None:
        return False, content

    filter_or_command = self.precompiler_mimetypes.get(mimetype)
    if filter_or_command is None:
        if mimetype in ("text/css", "text/javascript"):
            return False, content
        raise CompressorError("Couldn't find any precompiler in "
                              "COMPRESS_PRECOMPILERS setting for "
                              "mimetype '%s'." % mimetype)

    mod_name, cls_name = get_mod_func(filter_or_command)
    try:
        mod = import_module(mod_name)
    except (ImportError, TypeError):
        filter = CachedCompilerFilter(
            content=content, filter_type=self.type, filename=filename,
            charset=charset, command=filter_or_command, mimetype=mimetype)
        return True, filter.input(**kwargs)
    try:
        precompiler_class = getattr(mod, cls_name)
    except AttributeError:
        raise FilterDoesNotExist('Could not find "%s".' % filter_or_command)
    filter = precompiler_class(
        content, attrs=attrs, filter_type=self.type, charset=charset,
        filename=filename, **kwargs)
    return True, filter.input(**kwargs)


def filter(self, content, filters, method, **kwargs):
    for filter_cls in filters:
        filter_func = getattr(
            filter_cls(content, filter_type=self.type), method)
        try:
            if callable(filter_func):
                content = filter_func(**kwargs)
        except NotImplementedError:
            pass
    return content
