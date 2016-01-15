
from django.conf.urls import patterns, url, include
from .. import settings as media_settings
from .. import views

urlpatterns = patterns('',
                       url(
                           media_settings.MEDIA_CANONICAL_URL +
                           # flake8: noqa
                           r'(?P<uploaded_at>[0-9]+)/(?P<file_id>[0-9]+)/$',
                           views.canonical,
                           name='canonical'
                       ),
                       url(r'^' + media_settings.FILER_PRIVATEMEDIA_STORAGE.base_url.lstrip('/'),
                           include('leonardo.module.media.server.main_server_urls')),
                       url(r'^' + media_settings.FILER_PRIVATEMEDIA_THUMBNAIL_STORAGE.base_url.lstrip('/'),
                           include('leonardo.module.media.server.thumbnails_server_urls')),
                       )
