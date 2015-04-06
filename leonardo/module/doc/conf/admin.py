
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items

doc_options = []

try:
    doc_options.append(items.MenuItem(_('Documents'), reverse('webcms_admin:doc_document_changelist')))
except:
    pass

try:
    doc_options.append(items.MenuItem(_('Business entities'), reverse('webcms_admin:business_entity_changelist')))
except:
    pass

doc_menu = items.MenuItem(_('Document management'), reverse('webcms_admin:doc_document_changelist'), description=_('Complete electronic store management and utilities.'), children=doc_options),
