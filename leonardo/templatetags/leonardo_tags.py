
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


@register.simple_tag(takes_context=True)
def feincms_render_region(context, feincms_object, region, request=None):
    """
    {% feincms_render_region feincms_page "main" request %}
    """
    edit = ''
    if getattr(settings, 'LEONARDO_USE_PAGE_ADMIN', False):
        request = context.get('request', None)
        if request and request.COOKIES.get(
                'frontend_editing', False):
            url = reverse("widget_create", args=[feincms_object.id, region])
            edit = """<div class="clearfix col-md-12 region-tools"><a href="{0}" class='btn btn-block btn-success ajax-modal'>{1}</a></div>""".format(
                url, _('Add'))
    return ''.join(
        _render_content(content, request=request, context=context)
        for content in getattr(feincms_object.content, region)) + edit
