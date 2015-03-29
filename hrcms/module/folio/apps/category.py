from django.conf.urls.defaults import *

urlpatterns = patterns('webcms.module.folio.views',
    (r'^$', 'project_category_list', {}, 'webcms_folio_project_list'),
    (r'^(?P<category_slug>[0-9a-z\-]+)/$', 'project_category_list', {}, 'webcms_folio_project_list'),
    (r'^(?P<category_slug>[0-9a-z\-]+)/(?P<project_slug>[0-9a-z\-]+)/$', 'project_category_detail', {}, 'webcms_folio_project_detail'),
)
