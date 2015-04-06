from django.conf.urls.defaults import *

urlpatterns = patterns('webcms.module.doc.views',
    (r'^$', 'document_list', {}, 'webcms_document_list'),
    (r'^(?P<object_id>[\-\w]+)/$', 'document_detail', {}, 'webcms_document_detail'),
    (r'^(?P<object_id>[\-\w]+)/(?P<format>[\-\w]+)/$', 'document_file', {}, 'webcms_document_file'),
)
