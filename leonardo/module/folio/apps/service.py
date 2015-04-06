from django.conf.urls.defaults import *

urlpatterns = patterns('webcms.module.folio.views',
    (r'^$', 'project_list_service'),
    (r'^(?P<service_slug>[0-9a-z\-]+)/$', 'project_list_service'),
)
