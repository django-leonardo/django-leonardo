
from django.conf.urls import include, patterns, url
from oscarapi.app import application as api

# eshop API
urlpatterns = patterns('',
                       url(r'', include(api.urls)),
                       )
