# -*- coding: utf-8 -*-
"""JSONResponse views for model widgets."""
from __future__ import absolute_import, unicode_literals

import logging

from django.http import JsonResponse
from django.utils.encoding import smart_text
from django_select2.views import AutoResponseView

LOG = logging.getLogger(__name__)


class Select2ResponseView(AutoResponseView):

    """
    Temporary solution for rendering field label
    """

    def get(self, request, *args, **kwargs):
        """
        Return a :class:`.django.http.JsonResponse`.

        PR: https://github.com/applegrew/django-select2/pull/208

        Example::

            {
                'results': [
                    {
                        'text': "foo",
                        'id': 123
                    }
                ]
            }

        """
        self.widget = self.get_widget_or_404()

        if not self.widget:
            LOG.warning('Select2 field was not found, check your CACHE')

        self.term = kwargs.get('term', request.GET.get('term', ''))
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        label_fn = self.widget.label_from_instance if hasattr(
            self.widget, 'label_from_instance') else smart_text

        return JsonResponse({
            'results': [
                {
                    'text': label_fn(obj),
                    'id': obj.pk,
                }
                for obj in context['object_list']
            ],
        })
