

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

from roboticeclient.common.horizon import DjangoClient
from roboticeclient.control.v1.base import RoboticeControlClient

log = logging.getLogger('utils.robotice_client')

# only change base client class
RoboticeControlClient.client_class = DjangoClient

robotice_client = RoboticeControlClient(type="control")

class PortalView(tables.DataTableView):
    table_class = DeviceTable
    template_name = "portal/device_catalog/index.html"

    def get_data(self):

        devices = []

        devices = robotice_client.devices.list(self.request)

        return devices