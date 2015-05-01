
from __future__ import unicode_literals

from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from feincms.templatetags.feincms_tags import _render_content

register = template.Library()


@register.simple_tag
def get_col_classes(page, region):
    data = page.get_col_classes(region)
    if str(data) == "":
        return 'col-md-12'
    else:
        return data


@register.inclusion_tag('leonardo/common/_region_tools.html',
                        takes_context=True)
def render_region_tools(context, feincms_object, region, request=None):
    """
    {% render_region_tools feincms_page "main" request %}
    """
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
        'region': region
    }


@register.simple_tag(takes_context=True)
def feincms_render_region(context, feincms_object, region, request=None):
    """
    {% feincms_render_region feincms_page "main" request %}
    """
    return ''.join(
        _render_content(content, request=request, context=context)
        for content in getattr(feincms_object.content, region))
