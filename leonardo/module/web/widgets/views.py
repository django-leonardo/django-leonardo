
from __future__ import absolute_import

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from horizon import messages
from horizon_contrib.forms.views import (ContextMixin, CreateView,
                                         ModalFormView, ModelFormMixin,
                                         UpdateView)

from .forms import (get_widget_create_form, get_widget_update_form,
                    WidgetDeleteForm, WidgetSelectForm, WidgetUpdateForm)
from .tables import WidgetDimensionTable


class WidgetViewMixin(object):

    def handle_dimensions(self, obj):
        """save dimensions
        """
        from .tables import WidgetDimensionFormset
        from ..models import WidgetDimension
        formset = WidgetDimensionFormset(
            self.request.POST, prefix='dimensions')
        for form in formset.forms:
            if form.is_valid():
                if 'id' in form.cleaned_data:
                    form.save()
            else:
                # little ugly
                data = form.cleaned_data
                data['widget_type'] = \
                    ContentType.objects.get_for_model(obj)
                data['widget_id'] = obj.id
                data.pop('DELETE')
                wd = WidgetDimension(**data)
                wd.save()
        return True


class WidgetUpdateView(ModalFormView, UpdateView, WidgetViewMixin):

    template_name = 'leonardo/common/modal.html'

    form_class = WidgetUpdateForm

    def get_context_data(self, **kwargs):
        context = super(WidgetUpdateView, self).get_context_data(**kwargs)
        return context

    def get_form(self, form_class):
        """Returns an instance of the form to be used in this view."""

        kwargs = self.get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return get_widget_update_form(**self.kwargs)(**kwargs)

    def form_valid(self, form):
        response = super(WidgetUpdateView, self).form_valid(form)
        obj = self.object
        self.handle_dimensions(obj)
        return response


class WidgetCreateView(ModalFormView, CreateView, WidgetViewMixin):

    template_name = 'leonardo/common/modal.html'

    def get_label(self):
        return ugettext("Create new Widget")

    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        return get_widget_create_form(**self.kwargs)(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(WidgetCreateView, self).get_context_data(**kwargs)
        context['table'] = WidgetDimensionTable(self.request, data=[])
        # add extra context for template
        context['url'] = reverse("widget_create_full", kwargs=self.kwargs)
        return context

    def form_valid(self, form):
        try:
            obj = form.save(commit=False)
            obj.ordering = obj.next_ordering
            obj.save()
            obj.parent.save()
            success_url = self.get_success_url()
            response = HttpResponseRedirect(success_url)
            response['X-Horizon-Location'] = success_url
        except Exception, e:
            raise e

        return response

    def get_initial(self):
        return self.kwargs


class WidgetPreCreateView(ModalFormView, CreateView):

    form_class = WidgetSelectForm

    template_name = 'leonardo/common/modal.html'

    def get_label(self):
        return ugettext("Create new Widget")

    def get_context_data(self, **kwargs):
        context = super(WidgetPreCreateView, self).get_context_data(**kwargs)
        context['modal_size'] = 'modal-sm'
        return context

    def get_form(self, form_class):
        """Returns an instance of the form to be used in this view."""
        kwargs = self.kwargs
        kwargs.update(self.get_form_kwargs())
        kwargs.update({
            'request': self.request,
            'next_view': WidgetCreateView
        })
        return form_class(**kwargs)


class WidgetInfoView(ModalFormView, UpdateView, WidgetViewMixin):

    template_name = 'leonardo/common/modal.html'

    form_class = WidgetUpdateForm

    def get(self, request, cls_name, id):

        widget_info = """<span>{name}</span>""".format(**{
            'name': self.object
            })

        messages.info(request, mark_safe(widget_info))

        return HttpResponse(mark_safe(widget_info))


class WidgetDeleteView(ModalFormView, ContextMixin, ModelFormMixin):

    form_class = WidgetDeleteForm

    template_name = 'leonardo/common/modal.html'

    def get_label(self):
        return ugettext("Delete")  # .format(self.object.label))

    def get_context_data(self, **kwargs):
        context = super(WidgetDeleteView, self).get_context_data(**kwargs)

        # add extra context for template
        context['url'] = self.request.build_absolute_uri()
        context['modal_header'] = self.get_header()
        context['title'] = self.get_header()
        context['view_name'] = self.get_label()
        context['heading'] = self.get_header()
        context['help_text'] = self.get_help_text()
        return context

    def form_valid(self, form):
        obj = self.object
        try:
            parent = obj.parent
            obj.delete()
            # invalide page cache
            parent.invalidate_cache()
            success_url = parent.get_absolute_url()
            response = HttpResponseRedirect(success_url)
            response['X-Horizon-Location'] = success_url
        except Exception, e:
            raise e

        return response

    def get_initial(self):
        return self.kwargs
