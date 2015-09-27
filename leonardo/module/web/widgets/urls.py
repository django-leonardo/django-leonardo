
from __future__ import absolute_import

from django.conf.urls import patterns, url

from .views import *


urlpatterns = patterns('',
                       url(r'^(?P<page_id>[\w\.\-]+)/(?P<region>[\w\.\-]+)/(?P<cls_name>[\w\.\-]+)/select-widget/$',
                           WidgetPreCreateView.as_view(), name='widget_create'),
                       url(r'^(?P<page_id>[\w\.\-]+)/(?P<region>[\w\.\-]+)/(?P<cls_name>[\w\.\-]+)/(?P<ordering>[\w\.\-]+)/(?P<parent>[\w\.\-]+)/create/$',
                           WidgetCreateView.as_view(), name='widget_create_full'),
                       url(r'^(?P<cls_name>[\w\.\-]+)/(?P<id>[\w\.\-]+)/update/$',
                           WidgetUpdateView.as_view(), name='widget_update'),
                       url(r'^(?P<cls_name>[\w\.\-]+)/(?P<id>[\w\.\-]+)/delete/$',
                           WidgetDeleteView.as_view(), name='widget_delete'),
                       url(r'^(?P<cls_name>[\w\.\-]+)/(?P<id>[\w\.\-]+)/info/$',
                           WidgetInfoView.as_view(), name='widget_info'),
                       url(r'^(?P<cls_name>[\w\.\-]+)/(?P<id>[\w\.\-]+)/(?P<ordering>[\w\.\-]+)/ordering/$',
                           WidgetReorderView.as_view(), name='widget_reorder'),
                       url(r'^widget-sort/$',
                           WidgetSortView.as_view(), name='widget_sort'),
                       )
