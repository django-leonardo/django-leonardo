
from haystack.query import SearchQuerySet
from haystack.views import SearchView
from haystack.forms import ModelSearchForm


class LeonardoSearchView(SearchView):
    template_name = 'search/search.html'
    queryset = SearchQuerySet()
    form_class = ModelSearchForm
