
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import horizon

class CommonPanels(horizon.PanelGroup):
    slug = "device_catalog"
    name = _("Devices")
    panels = ('device_catalog', )

class PortalDashboard(horizon.Dashboard):
    name = _("Portal")
    slug = "portal"
    
    panels = (CommonPanels,)

    default_panel = 'device_catalog'

horizon.register(PortalDashboard)
