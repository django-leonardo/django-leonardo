from django.conf.urls import include, patterns, url

from .views import PluginInstallView

urlpatterns = patterns('',
                       url(r'^plugin-install/$',
                           PluginInstallView.as_view(), name='plugin_install'),
                       )
