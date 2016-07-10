from __future__ import absolute_import, unicode_literals

import logging

from django.http import Http404
from django.utils.functional import cached_property
from leonardo.module.web.widgets.utils import get_widget_from_id

from feincms import settings
from feincms._internal import get_model
from feincms.module.mixins import ContentView
from django.http import JsonResponse

logger = logging.getLogger(__name__)


class Handler(ContentView):

    """This is the main view for all pages

    In default state just render best match path

    Support AJAX widget calling for rendering regions and single widgets
    Also support calling custom methods on widgets with checking permissions on page level
    """

    page_model_path = None
    context_object_name = 'feincms_page'

    @cached_property
    def page_model(self):
        model = self.page_model_path or settings.FEINCMS_DEFAULT_PAGE_MODEL
        return get_model(*model.split('.'))

    def get_object(self):
        path = None
        if self.args:
            path = self.args[0]
        return self.page_model._default_manager.for_request(
            self.request, raise404=True, best_match=True, path=path)

    def render_widget(self, request, widget_id):
        '''Returns rendered widget in JSON response'''

        widget = get_widget_from_id(widget_id)

        response = widget.render(**{'request': request})

        return JsonResponse({'result': response, 'id': widget_id})

    def render_region(self, request):
        '''Returns rendered region in JSON response'''

        page = self.get_object()

        try:
            region = request.POST['region']
        except KeyError:
            region = request.GET['region']

        from leonardo.templatetags.leonardo_tags import _render_content
        request.query_string = None
        result = ''.join(
            _render_content(content, request=request, context={})
            for content in getattr(page.content, region))
        return JsonResponse({'result': result, 'region': region})

    def handle_ajax_method(self, request, method):
        """handle ajax methods and return serialized reponse

        - Depends on method parameter render whole region or single widget

        - If widget_id is present then try to load this widget and call method on them

        - If class_name is present then try to load class and then call static method on this class

        TODO: check permissions
        """

        response = {}

        def get_param(request, name):

            try:
                return request.POST[name]
            except KeyError:
                return request.GET.get(name, None)

        widget_id = get_param(request, "widget_id")
        class_name = get_param(request, "class_name")

        if method in 'widget_content':
            return self.render_widget(request, widget_id)

        if method == 'region':
            return self.render_region(request)

        # handle methods called directly on widget
        if widget_id:

            widget = get_widget_from_id(widget_id)

            try:
                func = getattr(widget, method)
            except AttributeError:
                response["exception"] = "%s method is not implmented on %s" % (method, widget)
            else:
                response["result"] = func(request)

        elif class_name:

            try:
                cls = get_model(*class_name.split('.'))
                func = getattr(cls, method)
            except Exception:
                response["exception"] = str(e)
            else:
                response["result"] = func(request)

        return JsonResponse(response)

    def get_method_for_ajax(self, request):
        """return method parameter from request only if is AJAX
        """
        if request.is_ajax():
            return request.GET.get('method', request.POST.get('method', None))


    def dispatch(self, request, *args, **kwargs):

        method = self.get_method_for_ajax(request)

        if method:
            # handle AJAX calls

            return self.handle_ajax_method(request, method)

        try:
            return super(Handler, self).dispatch(request, *args, **kwargs)
        except Http404 as e:
            if settings.FEINCMS_CMS_404_PAGE is not None:
                logger.info(
                    "Http404 raised for '%s', attempting redirect to"
                    " FEINCMS_CMS_404_PAGE", args[0])
                try:
                    # Fudge environment so that we end up resolving the right
                    # page.
                    # Note: request.path is used by the page redirect processor
                    # to determine if the redirect can be taken, must be == to
                    # page url.
                    # Also clear out the _feincms_page attribute which caches
                    # page lookups (and would just re-raise a 404).
                    request.path = request.path_info =\
                        settings.FEINCMS_CMS_404_PAGE
                    if hasattr(request, '_feincms_page'):
                        delattr(request, '_feincms_page')
                    response = super(Handler, self).dispatch(
                        request, settings.FEINCMS_CMS_404_PAGE, **kwargs)
                    # Only set status if we actually have a page. If we get for
                    # example a redirect, overwriting would yield a blank page
                    if response.status_code == 200:
                        response.status_code = 404
                    return response
                except Http404:
                    logger.error(
                        "Http404 raised while resolving"
                        " FEINCMS_CMS_404_PAGE=%s",
                        settings.FEINCMS_CMS_404_PAGE)
                    raise e
            else:
                raise
