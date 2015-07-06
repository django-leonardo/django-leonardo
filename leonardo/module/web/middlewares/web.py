
from django.conf import settings
from horizon import conf

from ..models import Page


class WebMiddleware(object):

    """add extra context to request

    added some extra to request and page

    .. code-block:: python

        request.leonardo_options

        request.LEONARDO_CONFIG

        request.leonardo_page

    supports this syntax

    .. code-block:: python

        request.LEONARDO_CONFIG.DISQUS_COMMENTS

    note: for support old ``webcms`` stuff adds some
    extra stuff which would be old after migration

    """

    def process_response(self, request, response):

        if hasattr(request, 'user') and not request.user.is_authenticated():
            response.delete_cookie('frontend_editing')
            request.frontend_editing = False
        return response

    def process_request(self, request):
        try:
            leonardo_options = {
                'meta_description': settings.META_DESCRIPTION,
                'meta_keywords': settings.META_KEYWORDS,
                'meta_title': settings.META_TITLE,
            }
        except:
            leonardo_options = {
                'meta_description': '',
                'meta_keywords': '',
                'meta_title': '',
            }

        leonardo_options['site'] = {
            'name': settings.SITE_NAME,
            'id': settings.SITE_ID,
            'domain': getattr(
                settings, 'SITE_DOMAIN', settings.SITE_NAME + '.cz'),
        }

        try:
            page = Page.objects.best_match_for_path(
                request.path)
        except Exception:
            page = None
            leonardo_options['template'] = 'base.html'
            leonardo_options['theme'] = 'light'
            leonardo_options['assets'] = []
            leonardo_options['widgets'] = []

        request.leonardo_options = leonardo_options
        request.leonardo_page = page

        request.frontend_editing = request.COOKIES.get(
            'frontend_editing', False)

        # basic support for multisite
        if getattr(settings, 'MULTI_SITE_ENABLED', False):
            Page.objects.active_filters.pop('current_site', None)
            Page.objects.add_to_active_filters(
                lambda queryset: queryset.filter(
                    site__name=str(request.get_host())),
                key='current_site')

        request.LEONARDO_CONFIG = conf.HORIZON_CONFIG

        # old
        request.webcms_page = page
        request.webcms_options = leonardo_options
