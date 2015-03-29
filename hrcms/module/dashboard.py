
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import horizon

class AuthPanels(horizon.PanelGroup):
    slug = "auth"
    name = _("Auth")
    panels = ('auth',)

class ModuleDashboard(horizon.Dashboard):
    name = _("Modules")
    slug = "module" # this map all to /

    panels = (AuthPanels,)

    default_panel = 'auth'

horizon.register(ModuleDashboard)
