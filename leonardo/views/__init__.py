from __future__ import absolute_import, unicode_literals

from horizon.tables.views import DataTableView  # noqa
from horizon.tables.views import MixedDataTableView  # noqa
from horizon.tables.views import MultiTableMixin  # noqa
from horizon.tables.views import MultiTableView  # noqa
from horizon_contrib.forms.views import (ContextMixin, ModalFormView,
                                         ModelFormMixin, UpdateView, CreateView)

from leonardo.apps import standalone

# set default template name
ModalFormView.template_name = 'leonardo/common/modal.html'

# mark all modal views as standalone
ModalFormView.get = standalone(ModalFormView.get)
UpdateView.get = standalone(UpdateView.get)
CreateView.get = standalone(CreateView.get)
