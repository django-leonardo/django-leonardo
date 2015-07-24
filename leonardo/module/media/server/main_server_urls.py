
from django.conf.urls import patterns, url


urlpatterns = patterns('leonardo.module.media.server.views',
                       url(r'^(?P<path>.*)$', 'serve_protected_file',),
                       )
