
from __future__ import absolute_import, unicode_literals

from django import template
from django.conf import settings
from django.core.urlresolvers import NoReverseMatch
from django.template import TemplateSyntaxError
from django.template.defaulttags import kwarg_re
from django.utils.encoding import smart_str
from django.utils.translation import ugettext as _
from feincms.templatetags.feincms_tags import _render_content
from feincms.templatetags.fragment_tags import (fragment, get_fragment,
                                                has_fragment)
from leonardo.module.web.widget.application.reverse import \
    app_reverse as do_app_reverse
from leonardo.module.web.widget.application.reverse import reverse_lazy

register = template.Library()

register.tag(fragment)
register.tag(get_fragment)
register.filter(has_fragment)


@register.simple_tag
def get_col_classes(page, region):
    data = page.get_col_classes(region)
    if str(data) == "":
        return 'col-md-12'
    else:
        return data


@register.simple_tag
def head_title(request):
    """
    {% head_title request %}
    """
    try:
        fragments = request._feincms_fragments
    except:
        fragments = {}

    if '_head_title' in fragments and fragments.get("_head_title"):
        return fragments.get("_head_title")
    else:
        return request.webcms_page.page_title


@register.inclusion_tag('leonardo/common/_region_tools.html',
                        takes_context=True)
def render_region_tools(context, feincms_object, region, request=None):
    """
    {% render_region_tools feincms_page "main" request %}

    skip rendering in standalone mode
    """

    if context.get('standalone', False) or not feincms_object:
        return {}

    edit = False

    if getattr(settings, 'LEONARDO_USE_PAGE_ADMIN', False):
        request = context.get('request', None)
        frontend_edit = request.COOKIES.get(
            'frontend_editing', False)
        if frontend_edit:
            edit = True

    return {
        'edit': edit,
        'feincms_object': feincms_object,
        'region': region,
        'widget_add_url': reverse_lazy(
            'widget_create',
            args=[feincms_object.id,
                  region,
                  '%s.%s' % (feincms_object._meta.app_label,
                             feincms_object.__class__.__name__)
                  ])
    }

STANDALONE_REGIONS = ['header', 'footer']


@register.simple_tag(takes_context=True)
def feincms_render_region(context, feincms_object, region, request=None):
    """
    {% feincms_render_region feincms_page "main" request %}

    Support for rendering Page without some regions especialy for modals
    this feature is driven by context variable
    """
    if not feincms_object:
        return ''

    if not context.get('standalone', False) or region in STANDALONE_REGIONS:
        return ''.join(
            _render_content(content, request=request, context=context)
            for content in getattr(feincms_object.content, region))
    return ''


class AppReverseNode(template.Node):

    def __init__(self, view_name, urlconf, args, kwargs, asvar):
        self.view_name = view_name
        self.urlconf = urlconf
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([
            (smart_str(k, 'ascii'), v.resolve(context))
            for k, v in self.kwargs.items()])
        view_name = self.view_name.resolve(context)
        urlconf = self.urlconf.resolve(context)

        try:
            url = do_app_reverse(
                view_name, urlconf, args=args, kwargs=kwargs,
                current_app=context.current_app)
        except NoReverseMatch:
            if self.asvar is None:
                raise
            url = ''

        if self.asvar:
            context[self.asvar] = url
            return ''
        else:
            return url


@register.tag
def app_reverse(parser, token):
    """
    Returns an absolute URL for applications integrated with ApplicationContent
    The tag mostly works the same way as Django's own {% url %} tag::
        {% load leonardo_tags %}
        {% app_reverse "mymodel_detail" "myapp.urls" arg1 arg2 %}
        or
        {% load leonardo_tags %}
        {% app_reverse "mymodel_detail" "myapp.urls" name1=value1 %}
    The first argument is a path to a view. The second argument is the URLconf
    under which this app is known to the ApplicationContent. The second
    argument may also be a request object if you want to reverse an URL
    belonging to the current application content.
    Other arguments are space-separated values that will be filled in place of
    positional and keyword arguments in the URL. Don't mix positional and
    keyword arguments.
    If you want to store the URL in a variable instead of showing it right away
    you can do so too::
        {% app_reverse "mymodel_detail" "myapp.urls" arg1 arg2 as url %}
    """
    bits = token.split_contents()
    if len(bits) < 3:
        raise TemplateSyntaxError(
            "'%s' takes at least two arguments"
            " (path to a view and a urlconf)" % bits[0])
    viewname = parser.compile_filter(bits[1])
    urlconf = parser.compile_filter(bits[2])
    args = []
    kwargs = {}
    asvar = None
    bits = bits[3:]
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]

    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError(
                    "Malformed arguments to app_reverse tag")
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))

    return AppReverseNode(viewname, urlconf, args, kwargs, asvar)


@register.tag
def url(parser, token):
    return app_reverse(parser, token)


@register.inclusion_tag('leonardo/common/_feincms_object_tools.html',
                        takes_context=True)
def feincms_object_tools(context, cls_name):
    """
    {% feincms_object_tools 'article' %}
    {% feincms_object_tools 'web.page' %}

    render add feincms object entry
    """
    if context.get('standalone', False):
        return {}
    edit = False
    if getattr(settings, 'LEONARDO_USE_PAGE_ADMIN', False):
        request = context.get('request', None)
        frontend_edit = request.COOKIES.get(
            'frontend_editing', False)
        if frontend_edit:
            edit = True

    return {
        'edit': edit,
        'add_entry_url': reverse_lazy(
            'horizon:contrib:forms:create',
            args=[cls_name])
    }
