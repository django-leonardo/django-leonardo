from django.conf.urls import *

urlpatterns = patterns('leonardo.module.media.views',
    (r'^$', 'directory_list_nested', {'directory_slug': None}),
    url(r'^fullscreen/(?P<category_id>[\w\-]+)/$', 'directory_detail_standalone', name="directory_detail_standalone"),
    (r'^(?P<directory_slug>[\w\-]+)/$', 'directory_list_nested'),
    (r'^(?P<parent_directory_slug>[\w\-]+)/(?P<directory_slug>[\w\-]+)/$', 'directory_list_nested'),
    (r'^(?P<grandparent_directory_slug>[\w\-]+)/(?P<parent_directory_slug>[\w\-]+)/(?P<directory_slug>[\w\-]+)/$', 'directory_list_nested'),
)
