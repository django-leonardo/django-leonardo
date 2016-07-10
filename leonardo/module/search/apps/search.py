

from django.conf.urls import patterns, url


try:
    from leonardo.module.search.forms import SearchForm
    from ..views import SearchView, SearchAutocomplete
except ImportError:
    raise Exception("Please install and configure haystack."
                    " Check your HAYSTACK_CONNECTIONS."
                    " This may fix pip install Whoosh"
                    " This is suitable backend only for development.")

urlpatterns = patterns('',
                       url(r'autocomplete/$', SearchAutocomplete.as_view(),
                           name='autocomplete_search'),
                       url(r'', SearchView(form_class=SearchForm),
                           name='haystack_search'),
                       )
