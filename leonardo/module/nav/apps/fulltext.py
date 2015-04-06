from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', include('haystack.urls'))
)
