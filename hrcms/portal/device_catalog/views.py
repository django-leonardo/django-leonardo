

from django.views.generic import TemplateView
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy

from horizon import tables
from horizon import exceptions
from horizon import forms
from horizon import tabs
from horizon import workflows
from horizon import messages

import logging

from django.conf import settings

from .tables import DeviceTable
from .forms import DummyForm

from .client import robotice_client

class PortalView(tables.DataTableView):
    table_class = DeviceTable
    template_name = "portal/device_catalog/index.html"

    def get_data(self):

        devices = []

        devices = robotice_client.devices.list(self.request)

        return devices

class DetailView(forms.ModalFormView):
    form_class = DummyForm
    template_name = 'portal/device_catalog/detail.html'
    success_url = reverse_lazy('horizon:portal:device_catalog:index')

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        context["device"] = robotice_client.devices.get(self.request, self.kwargs["id"])

        return context

    def get_initial(self):
        return {}