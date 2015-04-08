
from __future__ import absolute_import

from django.conf.urls import include, patterns, url

from leonardo.module.web.forms import get_widget_update_form
from horizon_contrib.forms.views import CreateView


class UpdateView(CreateView):
    form_class = None
    template_name = 'horizon_contrib/forms/create.html'

    name = ('Update')

    def get_form(self, form_class):
        """Returns an instance of the form to be used in this view."""
        return get_widget_update_form(**self.kwargs)(**self.get_form_kwargs())


urlpatterns = patterns('',
    url(r'^models/(?P<cls_name>[\w\.\-]+)/(?P<id>[\w\.\-]+)/update/$', UpdateView.as_view(), name='widget_update'),
)
