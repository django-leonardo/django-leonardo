

from crispy_forms.bootstrap import (Accordion, AccordionGroup, FieldWithButtons,
                                    StrictButton, Tab)
from crispy_forms.layout import Field, HTML, Layout, Submit
from crispy_forms.helper import FormHelper
from django.utils.translation import ugettext_lazy as _
from haystack.forms import ModelSearchForm


class SearchForm(ModelSearchForm):

    def _wrap_all(self):
        # stylung
        self.helper.filter(
            str, max_level=4).wrap(
            Field, css_class="form-control")

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            FieldWithButtons('q', Submit('submit', _("Search...")), css_class="col-xs-6 col-md-offset-3")
        )
