
from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from leonardo.views import *
from leonardo import messages

from leonardo.module.web.models import Page

from .forms import PageMassChangeForm


class PageObjectMixin(object):

    @property
    def object(self):

        try:
            obj = Page.objects.get(id=self.kwargs["page_id"])
        except Exception as e:
            messages.error(self.request, str(e))
        return obj


class PageMassUpdateView(PageObjectMixin, ModalFormView):

    """Page Mass Update of Theme, Color Scheme and Layout
    with custom depth
    """

    form_class = PageMassChangeForm

    def get_context_data(self, **kwargs):
        context = super(PageMassUpdateView, self).get_context_data(**kwargs)
        # add extra context for template
        context['url'] = self.request.build_absolute_uri()
        context['modal_header'] = _("Change Pages")
        context['form_submit'] = _("Apply")
        return context

    def form_invalid(self, form):
        raise Exception(form.errors)

    def get_initial(self):
        return {'page_id': self.kwargs["page_id"]}
