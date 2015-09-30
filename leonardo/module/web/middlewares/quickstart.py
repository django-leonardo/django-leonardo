
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import MiddlewareNotUsed
from leonardo.module.web.utils.scaffold_web import create_new_site
from ..models import Page


class QuickStartMiddleware(object):

    """Handle first start and provide initial content
    for quick start new site

    QuickStart is kicked up only once

    Populating content is separed into own module

    """

    def __init__(self):
        if Page.objects.count() == 0:
            raise MiddlewareNotUsed

    def process_response(self, request, response):

        # count pages as last option
        if response.status_code == 404 \
            and not hasattr(request, 'feincms_page') \
                and Page.objects.count() == 0:

            # use directory as first choice
            directory = getattr(settings, 'LEONARDO_BOOTSTRAP_DIR', None)
            if directory:
                url = None
            else:
                url = getattr(settings, 'LEONARDO_BOOTSTRAP_URL', None)

            page = create_new_site(request=request,
                                   url=url,
                                   run_syncall=True)

            return HttpResponseRedirect(reverse('page_update',
                                                kwargs={'page_id': page.pk}))

        return response
