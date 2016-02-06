
from ..models import Page


def add_page_if_missing(request):
    """
    Returns ``feincms_page`` for request.
    """

    try:
        page = Page.objects.for_request(request, best_match=True)
        return {
            'leonardo_page': page,
            # DEPRECATED
            'feincms_page': page,
        }
    except Page.DoesNotExist:
        return {}
