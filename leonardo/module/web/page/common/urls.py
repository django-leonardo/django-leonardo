
from __future__ import absolute_import

from django.conf.urls import patterns, url

from .views import PageMassUpdateView, PageCopyView

urlpatterns = patterns('',
                       url(r'^(?P<page_id>[\w\.\-]+)/theme$',
                           PageMassUpdateView.as_view(), name='page_mass_update'),
                       url(r'^(?P<cls_name>[\w\.\-]+)/(?P<id>[\w\.\-]+)/copy/$',
                           PageCopyView.as_view(), name='page_copy'),
                       )
