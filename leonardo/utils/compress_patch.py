from __future__ import unicode_literals, with_statement

import logging

from compressor.cache import cache_set
from compressor.conf import settings
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

    compress_tags.CompressorMixin.render_compressed = render_compressed
    compress_tags.CompressorMixin.render_output = render_output

    from django_pyscss import compressor as pyscss_compressor

    pyscss_compressor.DjangoScssFilter.input = input


def render_compressed(self, context, kind, mode, forced=False):

    # See if it has been rendered offline
    cached_offline = self.render_offline(context, forced=forced)
    if cached_offline:
        return cached_offline

    # Take a shortcut if we really don't have anything to do
    if ((not settings.COMPRESS_ENABLED and
         not settings.COMPRESS_PRECOMPILERS) and not forced):
        return self.get_original_content(context)

    context['compressed'] = {'name': getattr(self, 'name', None)}
    compressor = self.get_compressor(context, kind)

    # Prepare the actual compressor and check cache
    cache_key, cache_content = self.render_cached(
        compressor, kind, mode, forced=forced)
    if cache_content is not None:
        return cache_content

    # call compressor output method and handle exceptions
    try:
        rendered_output = self.render_output(
            compressor, mode, forced=forced, request=context.get('request'))
        if cache_key:
            cache_set(cache_key, rendered_output)
        assert isinstance(rendered_output, six.string_types)
        return rendered_output
    except Exception:
        if settings.DEBUG or forced:
            raise

    # Or don't do anything in production
    return self.get_original_content(context)


def render_output(self, compressor, mode, forced=False, request=None):
    return compressor.output(mode, forced=forced, request=request)


def input(self, **kwargs):
    """main override which append variables import to all scss content
    """

    with_variables = None

    try:
        page = kwargs['request'].leonardo_page
    except Exception as e:
        LOG.exception(str(e))
    else:
        with_variables = """
        @import "/themes/{}/{}/_variables";
        {}
        """.format(
            page.theme.name.lower(),
            page.color_scheme.name.lower(),
            self.content)

    return self.compiler.compile_string(
        with_variables or self.content,
        filename=self.filename)


def hunks(self, forced=False, request=None):
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
            'request': request,
        }

        if kind == SOURCE_FILE:
            options = dict(options, filename=value)
            value = self.get_filecontent(value, charset)

        if self.all_mimetypes:
            precompiled, value = self.precompile(value, **options)

        if enabled:
            yield self.filter(value, **options)
        else:
            if precompiled:
                yield self.handle_output(kind, value, forced=True,
                                         basename=basename)
            else:
                yield self.parser.elem_str(elem)


def output(self, mode='file', forced=False, request=None):
    """
    The general output method, override in subclass if you need to do
    any custom modification. Calls other mode specific methods or simply
    returns the content directly.
    """
    output = '\n'.join(self.filter_input(forced, request=request))

    if not output:
        return ''

    if settings.COMPRESS_ENABLED or forced:
        filtered_output = self.filter_output(output)
        return self.handle_output(mode, filtered_output, forced)

    return output


def filter_input(self, forced=False, request=None):
    """
    Passes each hunk (file or code) to the 'input' methods
    of the compressor filters.
    """
    content = []
    for hunk in self.hunks(forced, request=request):
        content.append(hunk)
    return content
