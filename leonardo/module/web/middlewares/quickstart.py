
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from leonardo.module.web.utils.scaffold_web import create_new_site
from ..models import Page


class QuickStartMiddleware(object):

    """Handle first start and provide initial content
    for quick start new site

    QuickStart is kicked up only once

    Populating content is separed into own module

    """

    def process_response(self, request, response):

        # TODO check page existence via request
        if response.status_code == 404 and Page.objects.count() == 0:

            page = create_new_site(request=request)

            return HttpResponseRedirect(reverse('page_update',
                                                kwargs={'page_id': page.pk}))

        if hasattr(request, 'user') and not request.user.is_authenticated():
            response.delete_cookie('frontend_editing')
            request.frontend_editing = False
        return response
