from django.conf.urls.defaults import *

urlpatterns = patterns('webcms.module.devel.views.auth',
    url(r'^user-perms/$', 'user_perms', name="webcms_devel_admin_user_perms"),
)
