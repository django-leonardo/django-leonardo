from django.conf import settings

from django import template, forms
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext as _
from django import template

from django.template import Library, Node, VariableDoesNotExist

from project.conf.menu import AdminMenu

from admin_tools.menu.templatetags.admin_tools_menu_tags import admin_tools_render_menu

register = template.Library()

from django import template

register = template.Library()

import glob

class TemplateStylesNode(template.Node):

    def __init__(self, template_name, location, editing):
        # saves the passed obj parameter for later use
        # this is a template.Variable, because that way it can be resolved
        # against the current context in the render method
        self.template_name = template.Variable(template_name)
        self.location = location.replace("'",'').replace('"','')
        self.editing = template.Variable(editing)

    def render(self, context):
        template_name = self.template_name.resolve(context)

        if self.location == "local":
            path = 'theme'
        else:
            path = 'lib/webcms-themes/%s' % template_name

        if self.editing:
            theme_path = '%s/%s/colors' % (settings.MEDIA_ROOT, path)
            theme_choices = []
            raw_choices = glob.glob('%s/*' % theme_path)
            for raw_choice in raw_choices:
                theme_choices.append(raw_choice.replace(theme_path, '').replace('/', '').replace('.css', ''))
            context['template_styles'] = theme_choices
            context['th'] = theme_path
            context['th2'] = raw_choices

        context['theme_path'] = '/media/%s' % path
        return ''

@register.tag
def set_template_styles(parser, token):
    try:
        tag_name, template_name, location, editing = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly three arguments" % token.contents.split()[0]
    return TemplateStylesNode(template_name, location, editing)
