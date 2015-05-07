

from crispy_forms.bootstrap import (Accordion, AccordionGroup, FieldWithButtons,
                                    StrictButton)
from crispy_forms.layout import Field, HTML, Layout
from django.utils.translation import ugettext_lazy as _
from haystack.forms import ModelSearchForm


class SearchForm(ModelSearchForm):

    def _wrap_all(self):
        # stylung
        self.helper.filter(
            basestring, max_level=4).wrap(
            Field, css_class="form-control")

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Accordion(
                AccordionGroup(_('Search'),
                               FieldWithButtons('q', StrictButton(_("Search")))
                               ),
                Tab(_('Options'),
                    Field('field_name_3', css_class="extra")
                    )
            )
        )

        self._wrap_all()
