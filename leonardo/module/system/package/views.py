
from __future__ import absolute_import

from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from horizon_contrib.forms.views import (ContextMixin, ModalFormView,
                                         ModelFormMixin, UpdateView)

from .forms import PluginInstallForm


class PluginInstallView(ModalFormView, ContextMixin, ModelFormMixin):

    form_class = PluginInstallForm

    template_name = 'leonardo/common/modal.html'

    def get_success_url(self):
        return self.request.build_absolute_uri()

    def get_context_data(self, **kwargs):
        context = super(PluginInstallView, self).get_context_data(**kwargs)

        context['url'] = self.request.build_absolute_uri()
        context['modal_header'] = _('Install Packages')
        context['title'] = _('Install')
        context['form_submit'] = _('Install')
        context['heading'] = _('Install Packages')
        return context

    def form_invalid(self, form):
        raise Exception(form.errors)
