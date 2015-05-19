

from django.conf.urls import patterns, url

from leonardo.module.search.forms import SearchForm
from haystack.views import SearchView


urlpatterns = patterns('',
                       url(r'', SearchView(form_class=SearchForm),
                           name='haystack_search'),
                       )
