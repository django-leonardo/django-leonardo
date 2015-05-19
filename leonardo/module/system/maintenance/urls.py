from django.conf.urls import include, patterns, url

from .views import ServerReloadView

urlpatterns = patterns('',
                       url(r'^server-reload/$',
                           ServerReloadView.as_view(), name='server_reload'),
                       )
