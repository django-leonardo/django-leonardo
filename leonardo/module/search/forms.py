

from crispy_forms.bootstrap import (Accordion, AccordionGroup, FieldWithButtons,
                                    StrictButton, Tab)
from crispy_forms.layout import Field, HTML, Layout
from crispy_forms.helper import FormHelper
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
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Accordion(
                Field('q', placeholder=_("Search"), css_class="form-control", wrapper_class='form-group'),
                StrictButton(_("Search"), type='submit', css_class="btn btn-default"),
                AccordionGroup(_('Options'),
                               Field('models')
                               )
            )
        )
