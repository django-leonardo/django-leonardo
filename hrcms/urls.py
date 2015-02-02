
import os

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, url, include
from django.contrib.auth.models import User, Group

from hrcms.views import IndexView

import horizon

admin.autodiscover()

urlpatterns = patterns('hrcms',
    
    url(r'^admin', include(admin.site.urls)),
    url(r'^doc/', include('django.contrib.admindocs.urls')),  

    #url(r'^$', IndexView.as_view(), name='index'),

    
    url(r'^accounts/', include('allauth.urls')),

    #url(r'^select2/', include('django_select2.urls')),

)

urlpatterns += patterns('',
    url(r'', include(horizon.urls)),
    url(r'', include('feincms.urls')),
)


urlpatterns += patterns('',
    url(r'^i18n/js/(?P<packages>\S+?)/$',
        'django.views.i18n.javascript_catalog',
        name='jsi18n'),
    url(r'^i18n/setlang/$',
        'django.views.i18n.set_language',
        name="set_language"),
    url(r'^i18n/', include('django.conf.urls.i18n'))
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)