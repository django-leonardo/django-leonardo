
from django import template

register = template.Library()

from elephantblog.models import Entry

@register.filter
def lang(items, lang):
    return items.filter(published__gt=40).filter(language=lang)

@register.filter
def count(items, count):
    return items.order_by('-published_on')[:count]