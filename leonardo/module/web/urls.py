
from __future__ import absolute_import

from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext
from horizon_contrib.forms.views import (ContextMixin, CreateView,
                                         ModalFormView, ModelFormMixin,
                                         UpdateView)
from horizon_contrib.generic.views import GenericIndexView
from leonardo.module.web.forms import (get_widget_create_form,
                                       get_widget_update_form)
from leonardo.module.web.models import Page

from .forms import WidgetCreatForm, WidgetDeleteForm

GenericIndexView.template_name = "leonardo/common/_index.html"


class UpdateView(ModalFormView, UpdateView):

    template_name = 'widget/create.html'

    def get_form(self, form_class):
        """Returns an instance of the form to be used in this view."""
        return get_widget_update_form(**self.kwargs)(**self.get_form_kwargs())

    def form_valid(self, form):
        response = super(UpdateView, self).form_valid(form)
        obj = self.object
        if not obj.prerendered_content:
            # turn off frontend edit for this redner
            request = self.request
            request.frontend_editing = False
            obj.prerendered_content = obj.render_content(
                options={'request': request})
            obj.save()
        return response


class CreateWidgetView(ModalFormView, CreateView):

    template_name = 'widget/create.html'

    def get_label(self):
        return ugettext("Create")

    def get_form(self, form_class):
        """Returns an instance of the form to be used in this view."""
        return get_widget_create_form(**self.kwargs)(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super(CreateWidgetView, self).get_context_data(**kwargs)

        # add extra context for template
        context['url'] = reverse("widget_create_full", kwargs=self.kwargs)
        return context

    def form_valid(self, form):
        try:
            obj = form.save()
            # invalide page cache
            page = Page.objects.get(id=self.kwargs['page_id'])
            page.invalidate_cache()

            if not obj.prerendered_content:
                # turn off frontend edit for this redner
                request = self.request
                request.frontend_editing = False
                obj.prerendered_content = obj.render_content(
                    options={'request': request})
                obj.save()

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


class DeleteWidgetView(ModalFormView, ContextMixin, ModelFormMixin):

    form_class = WidgetDeleteForm

    template_name = 'widget/create.html'

    def get_label(self):
        return ugettext("Delete")  # .format(self.object.label))

    def get_context_data(self, **kwargs):
        context = super(DeleteWidgetView, self).get_context_data(**kwargs)

        # add extra context for template
        context['url'] = self.request.build_absolute_uri()
        context['modal_header'] = self.get_header()
        context['title'] = self.get_header()
        context['view_name'] = self.get_label()
        context['heading'] = self.get_header()
        context['help_text'] = self.get_help_text()
        context['body'] = self.object.prerendered_content
        return context

    def form_valid(self, form):
        obj = self.object
        try:
            parent = obj.parent
            obj.delete()
            # invalide page cache
            page = Page.objects.get(id=parent.id)
            page.invalidate_cache()
            success_url = parent.get_absolute_url()
            response = HttpResponseRedirect(success_url)
            response['X-Horizon-Location'] = success_url
        except Exception, e:
            raise e

        return response

    def get_initial(self):
        return self.kwargs

urlpatterns = patterns('',
                       url(r'^models/(?P<page_id>[\w\.\-]+)/(?P<region>[\w\.\-]+)/create/$',
                           CreateView.as_view(), name='widget_create'),
                       url(r'^models/(?P<page_id>[\w\.\-]+)/(?P<region>[\w\.\-]+)/(?P<cls_name>[\w\.\-]+)/(?P<ordering>[\w\.\-]+)/(?P<parent>[\w\.\-]+)/create/$',
                           CreateWidgetView.as_view(), name='widget_create_full'),
                       url(r'^models/(?P<cls_name>[\w\.\-]+)/(?P<id>[\w\.\-]+)/update/$',
                           UpdateView.as_view(), name='widget_update'),
                       url(r'^models/(?P<cls_name>[\w\.\-]+)/(?P<id>[\w\.\-]+)/delete/$',
                           DeleteWidgetView.as_view(), name='widget_delete'),

                       )
