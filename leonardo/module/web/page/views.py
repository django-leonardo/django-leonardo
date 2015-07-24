
from __future__ import absolute_import

from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from leonardo.views import *
from leonardo import messages

from ..models import Page
from .dimension.forms import PageDimensionForm
from .tables import PageDimensionTable
from .forms import PageCreateForm, PageDeleteForm, PageUpdateForm


class PageCreateView(ModalFormView):

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
        context['modal_size'] = "lg"
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

    def get_initial(self):
        parent = self.parent
        initial = {
            'parent': parent,
            'slug': self.kwargs.get('slug', None),
            'color_scheme': parent.color_scheme,
            'theme': parent.theme,
            'layout': parent.layout,
            'site': parent.site,
            'template_key': parent.template_key,
            'in_navigation': parent.in_navigation,
        }
        if 'slug' in self.kwargs:
            initial['slug'] = self.kwargs['slug']
            initial['title'] = self.kwargs['slug'].capitalize()
        return initial


class PageUpdateView(ModalFormView):

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
        context['modal_size'] = "lg"
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

    def construct_tables(self):
        table = PageDimensionTable(
            self.request, data=self.object.dimensions.all())
        # Early out before data is loaded
        preempted = table.maybe_preempt()
        if preempted:
            return preempted

        # handle actions
        handled = table.maybe_handle()
        if handled:
            return handled

        # If we didn't already return a response, returning None continues
        # with the view as normal.
        return None

    def post(self, request, *args, **kwargs):
        # GET and POST handling are the same
        handled = self.construct_tables()
        if handled:
            return handled
        return super(PageUpdateView, self).post(request, *args, **kwargs)


class PageDimensionUpdateView(ModalFormView):

    form_class = PageDimensionForm

    @property
    def page(self):

        try:
            obj = Page.objects.get(id=self.kwargs["page_id"])
        except Exception as e:
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


class PageDeleteView(ModalFormView, ContextMixin, ModelFormMixin):

    form_class = PageDeleteForm

    @property
    def object(self):

        try:
            obj = Page.objects.get(id=self.kwargs["page_id"])
        except Exception as e:
            raise e
        return obj

    def get_context_data(self, **kwargs):
        context = super(PageDeleteView, self).get_context_data(**kwargs)

        page = self.object

        # add extra context for template
        context['url'] = self.request.build_absolute_uri()
        context['modal_header'] = 'Delete {} ?'.format(page)
        context['title'] = 'Delete {}'.format(page)
        context['form_submit'] = _('Delete')
        context['heading'] = 'Delete {} ?'.format(page)
        context['help_text'] = self.get_help_text()
        return context

    def form_valid(self, form):
        obj = self.object
        try:
            parent = obj.parent
            obj.delete()
            success_url = parent.get_absolute_url()
            response = HttpResponseRedirect(success_url)
            response['X-Horizon-Location'] = success_url
        except Exception as e:
            raise e

        return response

    def get_initial(self):
        return self.kwargs
