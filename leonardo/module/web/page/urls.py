
from __future__ import absolute_import

from django.conf.urls import include, patterns, url

from .views import *


urlpatterns = patterns('',
                       url(r'^(?P<page_id>[\w\.\-]+)/update/$',
                           PageUpdateView.as_view(), name='page_update'),
                       url(r'^(?P<parent>[\w\.\-]+)/create/$',
                           PageCreateView.as_view(), name='page_create'),
                       url(r'^(?P<page_id>[\w\.\-]+)/delete/$',
                           PageDeleteView.as_view(), name='page_delete'),
                       url(r'^(?P<parent>[\w\.\-]+)/(?P<slug>[\w\.\-]+)/create/$',
                           PageCreateView.as_view(), name='page_create'),
                       url(r'^(?P<page_id>[\w\.\-]+)/dimension/add/$',
                           PageDimensionUpdateView.as_view(), name='page_dimension_add'),
                       url(r'^change/', include('leonardo.module.web.page.common.urls')),
                       )
