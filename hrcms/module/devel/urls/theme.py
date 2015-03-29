from django.conf.urls.defaults import *

urlpatterns = patterns('webcms.module.devel.views.theme',
    url(r'^theme/$', 'theme_home', name="webcms_devel_admin_theme"),
    url(r'^css/$', 'css_list', name="webcms_devel_admin_css_list"),
    url(r'^css/(?P<file_name>[\w./]+)/$', 'css_edit', name="webcms_devel_admin_css_edit"),
)
