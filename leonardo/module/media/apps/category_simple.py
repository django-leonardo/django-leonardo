from django.conf.urls import *

urlpatterns = patterns('leonardo.module.media.views',
    (r'^$', 'category_list', {'category_slug': None, 'category_parent_slug': None}, 'leonardo_media_category_simple'),
    (r'^(?P<category_slug>[0-9a-zA-Z\-]+)/$', 'category_list', {'category_parent_slug': None}), 'leonardo_media_category_simple_level2',
)
