
from __future__ import absolute_import

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from horizon_contrib.forms.views import ModalFormView
from leonardo.module.web.forms import get_page_update_form

from ..forms import PageUpdateForm
from ..models import Page


class PageUpdateView(ModalFormView):

    template_name = 'widget/create.html'

    form_class = PageUpdateForm

    @property
    def object(self):

        try:
            obj = Page.objects.get(id=self.kwargs["page_id"])
        except Exception, e:
            raise e
        return obj

    def get_context_data(self, **kwargs):
        context = super(PageUpdateView, self).get_context_data(**kwargs)
        from ..tables import PageDimensionTable
        context['table'] = PageDimensionTable(
            self.request, page=self.object, data=self.object.own_dimensions)
        # add extra context for template
        context['url'] = self.request.build_absolute_uri()
        context['modal_header'] = _("Update Page")
        context['title'] = "self.get_header()"
        context['view_name'] = _("Update")
        context['heading'] = "self.get_header()"
        context['modal_size'] = "modal-lg"
        return context

    def handle_dimensions(self, obj):
        from ..tables import PageDimensionFormset
        from ..models import PageDimension
        formset = PageDimensionFormset(
            self.request.POST, prefix='dimensions')
        for form in formset.forms:
            if form.is_valid():
                form.save()
            else:
                # little ugly
                raise Exception(form.cleaned_data)
                data = form.cleaned_data
                data['widget_type'] = \
                    ContentType.objects.get_for_model(obj)
                data['widget_id'] = obj.id
                data.pop('DELETE')
                wd = PageDimension(**data)
                wd.save()
        return True

    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        kwargs.update({
            'request': self.request,
            'instance': self.object,
            'initial': {'page': self.object}
        })
        return get_page_update_form()(**kwargs)

    def form_valid(self, form):
        try:
            page = form.save()
            #self.handle_dimensions(page)
        except Exception as e:
            raise e
            # TODO push message
            # message.error(self.request, str(e))

        return HttpResponseRedirect(page.get_absolute_url())

    def form_invalid(self, form):
        raise Exception(form.errors)
