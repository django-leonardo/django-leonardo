
from __future__ import absolute_import

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from horizon_contrib.forms.views import ModalFormView

from leonardo import messages
from ..models import Page
from .dimension.forms import PageDimensionForm
from .forms import PageUpdateForm, PageCreateForm


class PageCreateView(ModalFormView):

    template_name = 'leonardo/common/modal.html'

    form_class = PageCreateForm

    @property
    def parent(self):

        try:
            obj = Page.objects.get(id=self.kwargs["parent"])
        except Exception as e:
            raise e
        return obj

    def get_context_data(self, **kwargs):
        context = super(PageCreateView, self).get_context_data(**kwargs)
        # add extra context for template
        context['url'] = self.request.build_absolute_uri()
        context['modal_header'] = _("Create Page")
        context['title'] = "self.get_header()"
        context['form_submit'] = _("Create")
        context['heading'] = "self.get_header()"
        context['modal_size'] = "modal-lg"
        return context

    def form_valid(self, form):
        try:
            page = form.save()
            messages.success(
                self.request, _('Page %s was successfully crated.' % page))
        except Exception as e:
            messages.error(self.request, str(e))
            return HttpResponseRedirect(self.object.get_absolute_url())

        return HttpResponseRedirect(page.get_absolute_url())

    def form_invalid(self, form):
        raise Exception(form.errors)

    def get_initial(self):
        parent = self.parent
        return {
            'parent': parent,
            'color_scheme': parent.color_scheme,
            'theme': parent.theme,
            'layout': parent.layout,
            'site': parent.site,
            'template_key': parent.template_key,
            'in_navigation': parent.in_navigation,
        }


class PageUpdateView(ModalFormView):

    template_name = 'leonardo/common/modal.html'

    form_class = PageUpdateForm

    @property
    def object(self):

        try:
            obj = Page.objects.get(id=self.kwargs["page_id"])
        except Exception as e:
            messages.error(self.request, str(e))
        return obj

    def get_context_data(self, **kwargs):
        context = super(PageUpdateView, self).get_context_data(**kwargs)
        # add extra context for template
        context['url'] = self.request.build_absolute_uri()
        context['modal_header'] = _("Update Page")
        context['title'] = "self.get_header()"
        context['form_submit'] = _("Update")
        context['heading'] = "self.get_header()"
        context['modal_size'] = "modal-lg"
        return context

    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        kwargs.update({
            'request': self.request,
            'instance': self.object,
            'initial': {'page': self.object}
        })
        return self.form_class(**kwargs)

    def form_valid(self, form):
        try:
            page = form.save()
        except Exception as e:
            messages.error(self.request, str(e))

        return HttpResponseRedirect(page.get_absolute_url())

    def form_invalid(self, form):
        raise Exception(form.errors)


class PageDimensionUpdateView(ModalFormView):

    template_name = 'leonardo/common/modal.html'

    form_class = PageDimensionForm

    @property
    def page(self):

        try:
            obj = Page.objects.get(id=self.kwargs["page_id"])
        except Exception, e:
            raise e
        return obj

    def get_context_data(self, **kwargs):
        context = super(PageDimensionUpdateView, self).get_context_data(**kwargs)
        # add extra context for template
        context['url'] = self.request.build_absolute_uri()
        context['modal_header'] = _("Add Page Dimesion")
        context['title'] = "self.get_header()"
        context['view_name'] = _("Create")
        context['heading'] = "self.get_header()"
        return context

    def get_initial(self):
        return {'page': self.page}

    def form_valid(self, form):
        try:
            dimension = form.save()
        except Exception as e:
            messages.error(self.request, str(e))

        return HttpResponseRedirect(dimension.page.get_absolute_url())

    def form_invalid(self, form):
        raise Exception(form.errors)
