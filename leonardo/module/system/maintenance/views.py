
from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from horizon_contrib.forms.views import (ContextMixin,
                                         ModalFormView, ModelFormMixin,
                                         UpdateView)
from .forms import ServerReloadForm


class ServerReloadView(ModalFormView, ContextMixin, ModelFormMixin):

    form_class = ServerReloadForm

    template_name = 'leonardo/common/modal.html'

    def get_success_url(self):
        return self.request.build_absolute_uri()

    def get_context_data(self, **kwargs):
        context = super(ServerReloadView, self).get_context_data(**kwargs)

        context['url'] = self.request.build_absolute_uri()
        context['modal_header'] = 'Reload Server'
        context['title'] = 'Reload Server'
        context['form_submit'] = _('Submit Reload')
        context['heading'] = 'Reload Server'
        return context
