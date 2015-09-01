
from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       url(r'^$', include('haystack.urls'))
                       )

from django.conf.urls.defaults import patterns, url

dict = {
    'template': 'googlesearch/googlesearch_results.html',
    'extra_context': {'title': 'Search Results'}
}

urlpatterns = patterns('django.views.generic.simple',
                       url(r'^$', 'direct_to_template', dict,
                           name='googlesearch_results'),
                       )
