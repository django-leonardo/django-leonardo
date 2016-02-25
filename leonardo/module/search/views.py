
from haystack.views import SearchView


class SearchView(SearchView):

    def extra_context(self):
        """
        Allows the addition of more context variables as needed.
        Must return a dictionary.
        """
        return {
            'widget': self.request._feincms_extra_context['widget']
        }
