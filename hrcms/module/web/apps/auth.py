"""
URLConf for Django user authentication.
"""
from django.conf.urls.defaults import patterns

urlpatterns = patterns('webcms.module.web.views.auth',
    (r'^$', 'login', {'template_name': 'auth/login.html'}, 'webcms_web_login'),
    (r'^password_reset/$', 'password_reset', {}, 'webcms_web_password_reset'),
    (r'^password_reset/done/$', 'password_reset_done', {'template_name':'auth/password_reset_done.html'}, 'webcms_web_password_reset_done'),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm', {}, 'webcms_web_password_reset_confirm'),
    (r'^reset/done/$', 'password_reset_complete', {}, 'webcms_web_password_reset_complete'),
    (r'^secure/$', 'login', {'SSL' : True, 'template_name': 'auth/login.html'}, 'webcms_web_secure_login'),
)

urlpatterns += patterns('django.contrib.auth.views',
    ('^logout/$','logout', {'template_name': 'auth/logout.html'}, 'webcms_web_logout'),
)

urlpatterns += patterns('webcms.module.web.views.auth',
)
