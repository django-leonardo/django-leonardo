
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
from django.utils.translation import ugettext_lazy as _, ugettext
from feincms import settings as feincms_settings
from feincms.module.page.extensions.navigation import PagePretender
from feincms.utils.templatetags import (do_simple_assignment_node_with_var_and_args_helper,
                                        do_simple_node_with_var_and_args_helper,
                                        SimpleAssignmentNodeWithVarAndArgs,
                                        SimpleNodeWithVarAndArgs)
from horizon_contrib.forms.models import create_or_update_and_get
from horizon_contrib.forms.views import CreateView, UpdateView, ModalFormView, ContextMixin
from leonardo.module.web.forms import get_widget_update_form
from leonardo.module.web.models import Page


from horizon_contrib.generic.views import GenericIndexView
from horizon_contrib.common import get_class

GenericIndexView.template_name = "leonardo/common/_index.html"

from .forms import WidgetCreatForm, WidgetDeleteForm


class UpdateView(ModalFormView, UpdateView):

    template_name = 'widget/create.html'

    def get_form(self, form_class):
        """Returns an instance of the form to be used in this view."""
        return get_widget_update_form(**self.kwargs)(**self.get_form_kwargs())


class CreateWidgetView(ModalFormView, CreateView):

    template_name = 'widget/create.html'

    def get_label(self):
        return ugettext("Create")

    def get_form(self, form_class):
        """Returns an instance of the form to be used in this view."""
        return get_widget_update_form(**self.kwargs)(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super(CreateWidgetView, self).get_context_data(**kwargs)

        # add extra context for template
        context['url'] = reverse("widget_create_full", kwargs=self.kwargs)
        return context

    def form_valid(self, form):
        try:
            form.save()
            # invalide page cache
            page = Page.objects.get(id = self.kwargs['page_id'])
            page.invalidate_cache()

            success_url = self.get_success_url()
            response = HttpResponseRedirect(success_url)
            response['X-Horizon-Location'] = success_url
        except Exception, e:
            raise e

        return response

    def get_initial(self):
        return self.kwargs


class CreateView(ModalFormView, CreateView):

    form_class = WidgetCreatForm

    template_name = 'widget/create.html'

    def get_label(self):
        return ugettext("Create")

    def get_form(self, form_class):
        """Returns an instance of the form to be used in this view."""
        kwargs = self.kwargs
        kwargs.update(self.get_form_kwargs())
        kwargs.update({
            'request': self.request,
            'next_view': CreateWidgetView
            })
        return form_class(**kwargs)


class DeleteWidgetView(ModalFormView, ContextMixin):

    form_class = WidgetDeleteForm

    template_name = 'widget/create.html'

    def get_label(self):
        return ugettext("Delete {}".format(self.kwargs['cls_name']))

    def get_context_data(self, **kwargs):
        context = super(DeleteWidgetView, self).get_context_data(**kwargs)

        # add extra context for template
        context['url'] = self.request.build_absolute_uri()
        context['modal_header'] = self.get_header()
        context['title'] = self.get_header()
        context['view_name'] = self.get_label()
        context['heading'] = self.get_header()
        context['help_text'] = self.get_help_text()
        return context

    def form_valid(self, form):
        try:
            cls = get_class(self.kwargs['cls_name'])
            obj = cls.objects.get(**{cls._meta.pk.name: self.kwargs['id']})
            parent = obj.parent
            obj.delete()
            # invalide page cache
            page = Page.objects.get(id = parent.id)
            page.invalidate_cache()

            success_url = self.get_success_url()
            response = HttpResponseRedirect(success_url)
            response['X-Horizon-Location'] = success_url
        except Exception, e:
            raise e

        return response

    def get_initial(self):
        return self.kwargs

urlpatterns = patterns('',
                       #url(r'^models/(?P<cls_name>[\w\.\-]+)/create/$',
                       #    CreateView.as_view(), name='widget_create'),
                       url(r'^models/(?P<page_id>[\w\.\-]+)/(?P<region>[\w\.\-]+)/create/$',
                           CreateView.as_view(), name='widget_create'),
                       url(r'^models/(?P<page_id>[\w\.\-]+)/(?P<region>[\w\.\-]+)/(?P<cls_name>[\w\.\-]+)/(?P<ordering>[\w\.\-]+)/(?P<parent>[\w\.\-]+)/create/$',
                           CreateWidgetView.as_view(), name='widget_create_full'),
                       url(r'^models/(?P<cls_name>[\w\.\-]+)/(?P<id>[\w\.\-]+)/update/$',
                           UpdateView.as_view(), name='widget_update'),
                       url(r'^models/(?P<cls_name>[\w\.\-]+)/(?P<id>[\w\.\-]+)/delete/$',
                           DeleteWidgetView.as_view(), name='widget_delete'),

                       )
