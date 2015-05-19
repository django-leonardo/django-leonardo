from django.conf.urls import include, patterns, url

from .views import ServerReloadView, ManagementView, InfoView

urlpatterns = patterns('',
                       url(r'^server-reload/$',
                           ServerReloadView.as_view(), name='server_reload'),
                       url(r'^management-commands/$',
                           ManagementView.as_view(), name='server_management'),
                       url(r'^system-info/$',
                           InfoView.as_view(), name='system_info'),
                       )
