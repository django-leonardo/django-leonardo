
from __future__ import absolute_import

from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from horizon_contrib.forms.views import (ContextMixin, CreateView,
                                         ModalFormView, ModelFormMixin,
                                         UpdateView)
from leonardo import messages
from leonardo import forms
import time

import django.dispatch

server_restart = django.dispatch.Signal(providing_args=["request", "wait"])

def server_restart_callback(request, wait=0, **kwargs):

    #time.sleep(wait)
    try:
        from django.utils.autoreload import restart_with_reloader
        restart_with_reloader()
        messages.success(
            request, _('Server was successfuly restarted !'))
    except Exception as e:
        messages.error(request, str(e))
    else:
        return True
    return False


server_restart.connect(server_restart_callback)


class ServerReloadForm(forms.SelfHandlingForm):

    wait = forms.IntegerField(label='wait before restart', initial=10, help_text=_('Time to wait before restart'))

    def handle(self, request, data):
        """PoC for self restart

        this support new abilities like an dynamic plugin install etc..
        """

        try:
            server_restart.send(sender=self.__class__,
                request=request, wait=data['wait'])
            messages.warning(
                request, _('Server going to down !'))
        except Exception as e:
            messages.error(request, str(e))
        else:
            return True
        return False


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
