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

tag_func = register.inclusion_tag('admin_tools/menu/dummy.html', takes_context=True)

@register.filter
def form_field(field, options = None):
    template = get_template('admin/form_field.html')
    c = Context({
        'field': field
    })
    return template.render(c)

def site_menu(context, menu='user'):
    if context.has_key('request'):
        request = context['request']
    else:
        request = False

    if menu == 'devel':
        menu = DevelAdminMenu()
    else:
        menu = AdminMenu()

    data = {
        'menu': menu,
        'request': request,
    }
    return data
register.inclusion_tag('admin/site_menu.html', takes_context=True)(site_menu)
