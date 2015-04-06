# -#- coding: utf-8 -#-

import os

from django.conf import settings
from django import template
from django.template.defaultfilters import escape
from django.contrib.sites.models import Site

register = template.Library()

@register.simple_tag
def webcms_site_logo():
    current_site = Site.objects.get_current()
    return "http://%s/static/theme/img/logo.png" % current_site.domain

@register.filter
def get_url(page):
    if page.__class__.__name__ == 'PagePretender':
        return page.url
    if page.redirect_to:
        return page.redirect_to
    elif page.template_key == 'layout_void':
        try:
            url = page.active_children()[0].get_navigation_url()
        except:
            url = '.'
        return url
    else:
        return page.get_absolute_url()

@register.simple_tag
def head_title(request):
    """
    {% head_title request %}
    """
    try:
        fragments = request._feincms_fragments
    except:
        fragments = {}

    if fragments.has_key("_head_title") and fragments.get("_head_title") != '':
        return fragments.get("_head_title")
    else:
        return request.webcms_page.page_title

@register.simple_tag
def body_classes(page):
    """
    {% body_classes webcms_page %}
    """
    if page.level == 1:
        trunk = page.slug
    elif page.level == 2:
        trunk = page.parent.slug
    elif page.level == 3:
        trunk = page.parent.parent.slug
    elif page.level == 4:
        trunk = page.parent.parent.parent.slug
    elif page.level == 5:
        trunk = page.parent.parent.parent.parent.slug
    else:
        trunk = page
    return u"page_%s trunk_%s" % (page.slug, trunk)

def google_analytics(account="default", type="async", filter="all"):
    types = ['sync', 'async', 'urchin']
    if not type in types:
        type = 'async'

    if account == "default":
        try:
            account = settings.GOOGLE_ANALYTICS
        except:
            account = False

    return {
        'account': account,
        'type': type,
        'filter': filter,
        'debug': settings.DEBUG
    }
register.inclusion_tag('base/google_analytics.html')(google_analytics)

def mod(value, arg):
    """
    Returns modulus for given integer.
    """
    return value % int(arg)
register.filter(mod)

def random_int(start, end):
    """
    Returns random number.
    """
    return random.randint(int(start), int(end))
register.simple_tag(random_int)

def truncchar(value, arg):
    """
    Truncates string after a given number of characters.
    """
    if len(value) < int(arg):
        return value
    else:
        return value[:int(arg)] + '…'
register.filter(truncchar)

def startswith(value, arg):
    """Usage, {% if value|startswith:"arg" %}"""
    return value.startswith(arg)
register.filter(startswith)

def endswith(value, arg):
    """Usage, {% if value|endswith:"arg" %}"""
    return value.endswith(arg)
register.filter(endswith)

def icontains(value, arg):
    """Usage, {% if value|contains:"arg" %}"""
    if value.find(arg) == -1:
        return False
    else:
        return True
register.filter(icontains)

def replace(value, arg1, arg2):
    """Usage, {{ value|replace:"arg1, arg2" }}"""
    return value.replace(arg1, arg2)
register.filter(replace)

@register.filter
def in_list(value,arg):
    '''
    Usage
    {% if value|in_list:list %}
    {% endif %}
    '''
    return value in arg

def _render_content(content, **kwargs):
    # Track current render level and abort if we nest too deep. Avoids
    # crashing in recursive page contents (eg. a page list that contains
    # itself or similar).
    request = kwargs.get('request')
    if request is not None:
        level = getattr(request, 'feincms_render_level', 0)
        if level > 10:
            # TODO: Log this
            return
        setattr(request, 'feincms_render_level', level + 1)

    kwargs['use_xml'] = True

    try:
        r = content.fe_render(**kwargs)
    except AttributeError:
        r = content.render(**kwargs)

    if request is not None:
        level = getattr(request, 'feincms_render_level', 1)
        setattr(request, 'feincms_render_level', max(level - 1, 0))

    return r

class RenderRegionNode(template.Node):
    def __init__(self, feincms_object, region, request):
        self.feincms_object = template.Variable(feincms_object)
        self.region = template.Variable(region)
        self.request = template.Variable(request)

    def render(self, context):
        feincms_object = self.feincms_object.resolve(context)
        region = self.region.resolve(context)
        request = self.request.resolve(context)

        return u''.join(_render_content(content, request=request, context=context)\
            for content in getattr(feincms_object.content, region))

@register.tag
def webcms_render_xml_region(parser, token):
    """
    {% webcms_render_xml_region page "main" request %}
    """
    try:
        tag_name, feincms_object, region, request = token.contents.split()
    except ValueError:
        raise template.TemplateSyntaxError, 'Invalid syntax for webcms_render_xml_region: %s' % token.contents

    return RenderRegionNode(feincms_object, region, request)

@register.filter(name="jsescape")
def jsescape(value) :
    if len(value.split(os.linesep)) > 1 :
        __s = ["\"%s\"" % escape(i) for i in value.split(os.linesep)]
        return "%s\n%s" % (__s[0], "\n".join([" + %s" % i for i in __s[1:]]), )
    else :
        return "\"%s\"" % escape(value)