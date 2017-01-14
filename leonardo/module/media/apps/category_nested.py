from django.conf.urls import *

urlpatterns = patterns('leonardo.module.media.views',
    url(r'^$', 'directory_list_nested', {'directory_slug': None}, name="directories"),
    url(r'^fullscreen/(?P<category_id>[\w\-]+)/$', 'directory_detail_standalone', name="directory_detail_standalone"),
    url(r'^(?P<directory_slug>.*)/$', 'directory_list_nested', name='directory_list_nested'),
    url(r'^(?P<parent_directory_slug>[\w\-]+)/(?P<directory_slug>[\w\-]+)/$', 'directory_list_nested', name="parent_directory_list_nested"),
    url(r'^(?P<grandparent_directory_slug>[\w\-]+)/(?P<parent_directory_slug>[\w\-]+)/(?P<directory_slug>[\w\-]+)/$', 'directory_list_nested'),
)
