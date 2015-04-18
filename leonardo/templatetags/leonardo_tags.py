
from django import template

register = template.Library()


@register.filter
def get_col_classes(page, region):
    return page.get_col_classes(region)
