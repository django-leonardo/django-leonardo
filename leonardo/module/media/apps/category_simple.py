from django.conf.urls import *

urlpatterns = patterns('leonardo.module.media.views',
                       (r'^$', 'directory_list', {
                        'directory_slug': None, 'category_parent_slug': None}, 'leonardo_media_category_simple'),
                       )
