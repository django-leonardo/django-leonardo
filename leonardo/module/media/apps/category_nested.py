from django.conf.urls.defaults import *

urlpatterns = patterns('webcms.module.media.views',
    (r'^$', 'category_list_nested', {'category_slug': None}),
    url(r'^fullscreen/(?P<category_id>[\w\-]+)/$', 'category_detail_standalone', name="webcms_media_category_detail_standalone"),
    (r'^(?P<category_slug>[\w\-]+)/$', 'category_list_nested'),
    (r'^(?P<parent_category_slug>[\w\-]+)/(?P<category_slug>[\w\-]+)/$', 'category_list_nested'),
    (r'^(?P<grandparent_category_slug>[\w\-]+)/(?P<parent_category_slug>[\w\-]+)/(?P<category_slug>[\w\-]+)/$', 'category_list_nested'),
)
