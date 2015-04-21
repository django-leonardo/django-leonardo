
from __future__ import absolute_import

import logging
import sys
import traceback

from django import template
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.core.urlresolvers import reverse
from django.db.models.loading import get_model
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from feincms import settings as feincms_settings
from feincms.module.page.extensions.navigation import PagePretender
from feincms.utils.templatetags import (do_simple_assignment_node_with_var_and_args_helper,
                                        do_simple_node_with_var_and_args_helper,
                                        SimpleAssignmentNodeWithVarAndArgs,
                                        SimpleNodeWithVarAndArgs)
from horizon_contrib.forms.models import create_or_update_and_get
from horizon_contrib.forms.views import CreateView, UpdateView
from leonardo.module.web.forms import get_widget_update_form
from leonardo.module.web.models import Page


class CreateView(CreateView):

    template_name = 'widget/create.html'

    def get_form(self, form_class):
        """Returns an instance of the form to be used in this view."""
        return get_widget_update_form(**self.kwargs)(**self.get_form_kwargs())

class UpdateView(UpdateView):

    template_name = 'widget/create.html'

    def get_form(self, form_class):
        """Returns an instance of the form to be used in this view."""
        return get_widget_update_form(**self.kwargs)(**self.get_form_kwargs())


urlpatterns = patterns('',
    url(r'^models/(?P<cls_name>[\w\.\-]+)/create/$', CreateView.as_view(), name='widget_create'),
    url(r'^models/(?P<cls_name>[\w\.\-]+)/(?P<id>[\w\.\-]+)/update/$', UpdateView.as_view(), name='widget_update'),
)
