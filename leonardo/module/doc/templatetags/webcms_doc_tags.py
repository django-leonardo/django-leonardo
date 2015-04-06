from django import template
from django.template.loader import render_to_string

from feincms import settings as feincms_settings
from feincms import utils

register = template.Library()

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

    try:
        r = content.fe_render(**kwargs)
    except AttributeError:
        r = content.render(**kwargs)

    if request is not None:
        level = getattr(request, 'feincms_render_level', 1)
        setattr(request, 'feincms_render_level', max(level - 1, 0))

    return r

class RenderRegionNode(template.Node):
    def __init__(self, feincms_object, region, format, request):
        self.feincms_object = template.Variable(feincms_object)
        self.region = template.Variable(region)
        self.request = template.Variable(request)
        self.format = template.Variable(format)

    def render(self, context):
        feincms_object = self.feincms_object.resolve(context)
        region = self.region.resolve(context)
        request = self.request.resolve(context)
        format = self.format.resolve(context)

        return u''.join(_render_content(content, format=format, request=request, context=context)\
            for content in getattr(feincms_object.content, region))

@register.tag
def webcms_render_region(parser, token):
    """
    {% webcms_render_region feincms_page "main" "html" request %}
    """
    try:
        tag_name, feincms_object, region, format, request = token.contents.split()
    except ValueError:
        raise template.TemplateSyntaxError, 'Invalid syntax for feincms_render_region: %s' % token.contents

    return RenderRegionNode(feincms_object, region, format, request)

class RenderContentNode(template.Node):
    def __init__(self, content, request):
        self.content = template.Variable(content)
        self.request = template.Variable(request)

    def render(self, context):
        content = self.content.resolve(context)
        request = self.request.resolve(context)

        return _render_content(content, request=request, context=context)
