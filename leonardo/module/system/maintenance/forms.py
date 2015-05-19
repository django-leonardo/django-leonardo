import os
import sys
from leonardo import messages
from leonardo import forms
from django.utils.translation import ugettext_lazy as _

import django.dispatch

server_restart = django.dispatch.Signal(providing_args=["request", "delay"])


def server_restart_callback(request, delay=0, **kwargs):

    # time.sleep(delay)
    try:

        #from django.utils.autoreload import restart_with_reloader, reloader_thread
        # kill self
        os.kill(os.getpid(), 9)

        messages.success(
            request, _('Server was successfuly restarted !'))
    except Exception as e:
        messages.error(request, str(e))
    else:
        return True
    return False


server_restart.connect(server_restart_callback)


class ServerReloadForm(forms.SelfHandlingForm):

    delay = forms.IntegerField(
        label=_('delay before restart'), initial=10, help_text=_('Delay before restart'))

    def handle(self, request, data):
        """PoC for self restart

        this support new abilities like an dynamic plugin install etc..
        """

        try:
            server_restart.send(sender=self.__class__,
                                request=request, delay=data['delay'])
            messages.warning(
                request, _('Server going to down !'))
        except Exception as e:
            messages.error(request, str(e))
        else:
            return True
        return False
