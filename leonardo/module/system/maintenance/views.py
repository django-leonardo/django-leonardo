
from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from leonardo.views import *
from .forms import ServerReloadForm, ManagementForm, InfoForm


class ServerReloadView(ModalFormView, ContextMixin, ModelFormMixin):

    form_class = ServerReloadForm

    def get_success_url(self):
        return self.request.build_absolute_uri()

    def get_context_data(self, **kwargs):
        context = super(ServerReloadView, self).get_context_data(**kwargs)

        context['url'] = self.request.build_absolute_uri()
        context['modal_header'] = 'Reload Server'
        context['title'] = 'Reload Server'
        context['form_submit'] = _('Submit Reload')
        context['heading'] = 'Reload Server'
        context['modal_size'] = 'sm'
        return context


class InfoView(ModalFormView, ContextMixin, ModelFormMixin):

    form_class = InfoForm

    def get_success_url(self):
        return self.request.build_absolute_uri()

    def get_form(self, form_class):
        """Returns an instance of the form to be used in this view."""

        kwargs = self.get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return form_class(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(InfoView, self).get_context_data(**kwargs)

        context['url'] = self.request.build_absolute_uri()
        context['modal_header'] = _('Leonardo Info')
        context['title'] = _('Leonardo Info')
        context['form_submit'] = _('Close')
        context['heading'] = _('Leonardo Info')
        context['modal_size'] = 'fullscreen'
        return context

    def form_invalid(self, form):
        raise Exception(form.errors)


class ManagementView(ModalFormView, ContextMixin, ModelFormMixin):

    form_class = ManagementForm

    def get_success_url(self):
        return self.request.build_absolute_uri()

    def get_context_data(self, **kwargs):
        context = super(ManagementView, self).get_context_data(**kwargs)

        context['url'] = self.request.build_absolute_uri()
        context['modal_header'] = _('Management commands')
        context['title'] = _('Management commands')
        context['form_submit'] = _('Run commands')
        context['heading'] = _('Management commands')
        context['modal_size'] = 'md'
        return context

    def form_invalid(self, form):
        raise Exception(form.errors)
