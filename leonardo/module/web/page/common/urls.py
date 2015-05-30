
from __future__ import absolute_import

from django.conf.urls import include, patterns, url

from .views import *

urlpatterns = patterns('',
                       url(r'^(?P<page_id>[\w\.\-]+)/theme$',
                           PageMassUpdateView.as_view(), name='page_mass_update'),
                       )
