
from django.utils.translation import ugettext_lazy as _

import horizon

from leonardo.module import dashboard


class AuthPanel(horizon.Panel):
    name = _("Auth")
    slug = 'auth'

#dashboard.ModuleDashboard.register(AuthPanel)
