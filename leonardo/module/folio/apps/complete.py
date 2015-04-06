from django.conf.urls.defaults import *

urlpatterns = patterns('webcms.module.folio.views',
    (r'^$', 'project_list', {}, 'webcms_folio_project_list'),
    (r'^service/(?P<category_slug>[0-9a-z\-]+)/$', 'category_detail', {}, 'webcms_folio_category_detail'),
    (r'^client/(?P<client_slug>[0-9a-z\-]+)/$', 'client_detail', {}, 'webcms_folio_client_detail'),
    (r'^(?P<project_slug>[0-9a-z\-]+)/$', 'project_detail', {}, 'webcms_folio_project_detail'),
)
