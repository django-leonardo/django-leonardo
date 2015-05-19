
from horizon.tables.views import DataTableView  # noqa
from horizon.tables.views import MixedDataTableView  # noqa
from horizon.tables.views import MultiTableMixin  # noqa
from horizon.tables.views import MultiTableView  # noqa
from horizon_contrib.forms.views import (ContextMixin, ModalFormView,
                                         ModelFormMixin, UpdateView, CreateView)

# set default template name
ModalFormView.template_name = 'leonardo/common/modal.html'
