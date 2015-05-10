
from __future__ import absolute_import

from horizon import Horizon
import horizon_contrib
from django.conf.urls import include, patterns, url

# horizon and feinCMS
urlpatterns = patterns('',
                       url(r'', include(Horizon._lazy_urls)),
                       url(r'', include(horizon_contrib.urls)),
                       )
