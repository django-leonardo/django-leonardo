
from __future__ import absolute_import

from django.conf.urls import include, patterns, url
from horizon_contrib.forms.views import (CreateView,
                                         UpdateView)
from horizon_contrib.generic.views import GenericIndexView

# override native horizon-contrib views
GenericIndexView.template_name = "leonardo/common/_index.html"
CreateView.template_name = "widget/create.html"
UpdateView.template_name = "widget/create.html"

from .views.widget import *
from .views.page import *


urlpatterns = patterns('',
                       url(r'^models/(?P<page_id>[\w\.\-]+)/(?P<region>[\w\.\-]+)/create/$',
                           WidgetPreCreateView.as_view(), name='widget_create'),
                       url(r'^models/(?P<page_id>[\w\.\-]+)/(?P<region>[\w\.\-]+)/(?P<cls_name>[\w\.\-]+)/(?P<ordering>[\w\.\-]+)/(?P<parent>[\w\.\-]+)/create/$',
                           WidgetCreateView.as_view(), name='widget_create_full'),
                       url(r'^models/(?P<cls_name>[\w\.\-]+)/(?P<id>[\w\.\-]+)/update/$',
                           WidgetUpdateView.as_view(), name='widget_update'),
                       url(r'^models/(?P<cls_name>[\w\.\-]+)/(?P<id>[\w\.\-]+)/delete/$',
                           WidgetDeleteView.as_view(), name='widget_delete'),
                       url(r'^redactor/', include('redactor.urls')),
                       url(r'^models/(?P<page_id>[\w\.\-]+)/update/$',
                           PageUpdateView.as_view(), name='page_update'),
                       )
