
from django.utils.translation import ugettext_lazy as _

import horizon

from hrcms.module import dashboard


class AuthPanel(horizon.Panel):
    name = _("Auth")
    slug = 'auth'
    
dashboard.ModuleDashboard.register(AuthPanel)
