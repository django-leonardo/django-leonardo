from distutils import version

from django.conf import settings
from django.template import Context, Template
from django.template.loader import get_template
from django import template

register = template.Library()

@register.filter
def form_errors(form):
    template = get_template('forms/errors.html')
    c = Context({'form':form})
    return template.render(c)

@register.filter
def form_field(field, options = None):
    template = get_template('forms/field.html')
    c = Context({
        'field': field,
    })
    return template.render(c)

@register.filter
def object_value(value, options = None):
    template = get_template('forms/value.html')
    c = Context({
        'value': value,
    })
    return template.render(c)

@register.simple_tag
def form_button(type, label, id = None):
    template = get_template('forms/button.html')
    c = Context({
        'type': type,
        'label': label,
        'id': id,
    })
    return template.render(c)
