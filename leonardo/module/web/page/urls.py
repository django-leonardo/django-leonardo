
from __future__ import absolute_import

from django.conf.urls import include, patterns, url

from .views import *


urlpatterns = patterns('',
                       url(r'^(?P<page_id>[\w\.\-]+)/update/$',
                           PageUpdateView.as_view(), name='page_update'),
                       url(r'^(?P<page_id>[\w\.\-]+)/dimension/add/$',
                           PageDimensionUpdateView.as_view(), name='page_dimension_add'),
                       )
