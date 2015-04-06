
from django.conf.urls import include, patterns, url
from oscar.app import application as oscar_app

# eshop
urlpatterns = patterns('',
                       url(r'', include(oscar_app.urls)),
                       )
