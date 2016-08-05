from __future__ import absolute_import, unicode_literals

import logging

from leonardo.module.web.widgets.utils import get_widget_from_id
from django.forms import modelform_factory
from feincms._internal import get_model
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)


class AJAXMixin(object):

    """Handle all AJAX calls

    Support AJAX widget calling for rendering regions and single widgets
    Also support calling custom methods on widgets with checking permissions on page level

    """

    def handle_ajax(self, request):

        method = self.get_method_for_ajax(request)

        if method:
            return self.handle_ajax_method(request, method)

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

        request.query_string = None

        from leonardo.utils.widgets import render_region

        result = render_region(page=page, request=request, region=region)

        return JsonResponse({'result': result, 'region': region})

    @method_decorator(login_required)
    def handle_ajax_method(self, request, method):
        """handle ajax methods and return serialized reponse
        in the default state allows only authentificated users

        - Depends on method parameter render whole region or single widget

        - If widget_id is present then try to load this widget
          and call method on them

        - If class_name is present then try to load class
          and then call static method on this class

        - If class_name is present then try to load class
          and if method_name == render_preview then
          render widget preview without instance

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
                response["exception"] = "%s method is not implmented on %s" % (
                    method, widget)
            else:
                response["result"] = func(request)

        elif class_name:
            # handle calling classmethod without instance

            try:
                cls = get_model(*class_name.split('.'))
            except Exception as e:
                response["exception"] = str(e)
                return JsonResponse(data=response)

            if method == "render_preview":

                # TODO: i think that we need only simple form
                # for loading relations but maybe this would be need it
                # custom_form_cls = getattr(
                #     cls, 'feincms_item_editor_form', None)

                # if custom_form_cls:
                #     FormCls = modelform_factory(cls, form=custom_form_cls,
                #                                 exclude=('pk', 'id'))

                FormCls = modelform_factory(cls, exclude=('pk', 'id'))

                form = FormCls(request.POST)

                if form.is_valid():

                    widget = cls(**form.cleaned_data)

                    request.frontend_editing = False

                    content = widget.render(**{'request': request})

                    response['result'] = content
                    response['id'] = widget_id

                else:
                    response['result'] = form.errors
                    response['id'] = widget_id

            else:
                # standard method
                try:
                    func = getattr(cls, method)
                except Exception as e:
                    response["exception"] = str(e)
                else:
                    response["result"] = func(request)

        return JsonResponse(data=response)

    def get_method_for_ajax(self, request):
        """return method parameter from request only if is AJAX
        """
        return request.GET.get('method', request.POST.get('method', None))
