from __future__ import absolute_import

from horizon.tables.views import DataTableView  # noqa
from horizon.tables.views import MixedDataTableView  # noqa
from horizon.tables.views import MultiTableMixin  # noqa
from horizon.tables.views import MultiTableView  # noqa
from horizon_contrib.forms.views import ModalFormView as DefaultModalFormView
from horizon_contrib.forms.views import (ContextMixin, CreateView,
                                         ModelFormMixin, UpdateView)

try:
    from feincms.views.decorators import standalone
except:
    from feincms.apps import standalone

# mark all modal views as standalone


class ModalViewMixin(object):

    def get_context_data(self, *args, **kwargs):
        context = super(ModalViewMixin, self).get_context_data(*args, **kwargs)
        context['standalone'] = True
        return context

    @standalone
    def get(self, *args, **kwargs):
        return super(ModalViewMixin, self).get(*args, **kwargs)


class ModalFormView(ModalViewMixin, DefaultModalFormView):

    # set default template name
    template_name = 'leonardo/common/modal.html'


class UpdateView(ModalViewMixin, UpdateView):

    pass


class CreateView(ModalViewMixin, CreateView):

    pass

__all__ = ('DataTableView', 'MixedDataTableView', 'MultiTableView',
           'MultiTableMixin', 'ContextMixin',
           'ModalFormView', 'UpdateView', 'CreateView',
           'ModelFormMixin')
