

from django.conf.urls import patterns, url

from leonardo.module.search.forms import SearchForm
from ..views import SearchView, SearchAutocomplete


urlpatterns = patterns('',
                       url(r'autocomplete/$', SearchAutocomplete.as_view(),
                           name='autocomplete_search'),
                       url(r'', SearchView(form_class=SearchForm),
                           name='haystack_search'),
                       )
