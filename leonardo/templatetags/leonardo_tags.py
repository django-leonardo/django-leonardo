
from django import template

register = template.Library()


@register.filter
def get_col_classes(page, region):
    data = page.get_col_classes(region)
    if str(data) == "":
    	return 'col-md-12'
    else:
    	return data
