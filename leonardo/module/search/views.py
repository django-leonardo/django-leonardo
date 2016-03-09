
import json
from haystack.views import SearchView
from django.views.generic import TemplateView
from django.http import HttpResponse
from haystack.query import SearchQuerySet


class SearchView(SearchView):

    def extra_context(self):
        """
        Allows the addition of more context variables as needed.
        Must return a dictionary.
        """
        return {
            'widget': self.request._feincms_extra_context['widget']
        }


class SearchAutocomplete(TemplateView):

    def get(self, *args, **kwargs):

        query = self.request.GET.get('q', '')

        sqs = SearchQuerySet().autocomplete(
            content_auto=query, title=query)[:5]

        suggestions = [result.title for result in sqs]
        # Make sure you return a JSON object, not a bare list.
        # Otherwise, you could be vulnerable to an XSS attack.
        the_data = json.dumps({
            'results': suggestions
        })
        return HttpResponse(the_data, content_type='application/json')
