
import copy

import floppyforms as forms
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import Field, HTML, Layout
from django.utils.translation import ugettext_lazy as _
from horizon.utils.memoized import memoized
from horizon_contrib.forms import SelfHandlingModelForm

from leonardo.module.web.models import PageDimension


class Slider(forms.RangeInput):
    min = 0
    max = 12
    step = 1


class PageDimensionForm(SelfHandlingModelForm):

    col1_width = forms.CharField(widget=Slider(), initial=4)
    col2_width = forms.CharField(widget=Slider(), initial=4)
    col3_width = forms.CharField(widget=Slider(), initial=4)

    def _check_dimensions(self):
        col1_width = self.cleaned_data['col1_width']
        col2_width = self.cleaned_data['col2_width']
        col3_width = self.cleaned_data['col3_width']
        if not (int(col1_width) + int(col2_width) + int(col3_width)) <= 12:
            raise forms.ValidationError(_("Summary of dimensions must be 12"))

    def clean(self):
        cleaned = super(PageDimensionForm, self).clean()
        self._check_dimensions()
        return cleaned

    class Meta:
        model = PageDimension
        exclude = tuple()
        widgets = {'page': forms.HiddenInput}
