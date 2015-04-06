
from django.utils.translation import ugettext_lazy as _

import horizon

from hrcms.portal import dashboard


class DeviceCatalogPanel(horizon.Panel):
    name = _("Device Catalog")
    slug = 'device_catalog'
    
dashboard.PortalDashboard.register(DeviceCatalogPanel)
