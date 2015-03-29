from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items

folio_options = [
    items.MenuItem(_('Projects'), reverse('webcms_admin:folio_project_changelist')),
    items.MenuItem(_('Extra properties'), reverse('webcms_admin:folio_attributeoption_changelist')),
    items.MenuItem(_('Categories'), reverse('webcms_admin:folio_category_changelist')),
    items.MenuItem(_('Clients'), reverse('webcms_admin:folio_client_changelist')),
    items.MenuItem(_('Services'), reverse('webcms_admin:folio_service_changelist')),
]
