from django.template import Library
from constance import config

register = Library()


def filer_staticmedia_prefix():
    """
    Returns the string contained in the setting FILER_STATICMEDIA_PREFIX.
    """
    try:
        from .. import settings
    except ImportError:
        return ''
    return settings.FILER_STATICMEDIA_PREFIX
filer_staticmedia_prefix = register.simple_tag(filer_staticmedia_prefix)


@register.filter
def files_order_by(queryset, order_by=None):

    order_by = order_by or config.MEDIA_FILES_ORDER_BY

    if order_by:
        queryset = queryset.order_by(*order_by.split(","))

    return queryset


@register.filter
def folders_order_by(queryset, order_by=None):

    order_by = order_by or config.MEDIA_FOLDERS_ORDER_BY

    if order_by:
        queryset = queryset.order_by(*order_by.split(","))

    return queryset
