
from __future__ import absolute_import

from django.conf.urls import include, patterns, url

from leonardo.module.web.forms import get_widget_update_form
from horizon_contrib.forms.views import CreateView


class CreateView(CreateView):

    template_name = 'widget/create.html'

    def get_form(self, form_class):
        """Returns an instance of the form to be used in this view."""
        return get_widget_update_form(**self.kwargs)(**self.get_form_kwargs())


class UpdateView(CreateView):

    def get_form(self, form_class):
        """Returns an instance of the form to be used in this view."""
        return get_widget_update_form(**self.kwargs)(**self.get_form_kwargs())


urlpatterns = patterns('',
    url(r'^models/(?P<cls_name>[\w\.\-]+)/create/$', CreateView.as_view(), name='widget_create'),
    url(r'^models/(?P<cls_name>[\w\.\-]+)/(?P<id>[\w\.\-]+)/update/$', UpdateView.as_view(), name='widget_update'),
)
