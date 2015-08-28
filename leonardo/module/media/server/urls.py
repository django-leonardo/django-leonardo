
from django.conf.urls import patterns, url, include
from .. import settings as filer_settings


urlpatterns = patterns('',
                       url(r'^' + filer_settings.FILER_PRIVATEMEDIA_STORAGE.base_url.lstrip('/'),
                           include('leonardo.module.media.server.main_server_urls')),
                       url(r'^' + filer_settings.FILER_PRIVATEMEDIA_THUMBNAIL_STORAGE.base_url.lstrip('/'),
                           include('leonardo.module.media.server.thumbnails_server_urls')),
                       )
