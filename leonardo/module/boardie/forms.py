
import floppyforms as forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Fieldset, Layout, Submit, Tab, TabHolder
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from feincms.module.page.models import Page
from feincms.views.decorators import standalone


class AngularSelect(forms.Select):
    template_name = 'angular_form/select.html'


class AngularRadioButton(forms.Select):
    template_name = 'angular_form/radiobutton.html'


class AngularTextInput(forms.TextInput):
    template_name = 'angular_form/input.html'


class AngularTextarea(forms.Textarea):
    template_name = 'angular_form/textarea.html'


class AngularToggleButton(forms.Select):
    template_name = 'angular_form/togglebutton.html'


class AngularCheckBox(forms.Select):
    template_name = 'angular_form/checkbox.html'


class DashboardForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = [
            'title',
            'override_url',
        ]
        widgets = {
            'title': AngularTextInput(attrs={'autofocus': True}),
            'override_url': AngularTextInput,
        }

    def __init__(self, *args, **kwargs):
        super(DashboardForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            TabHolder(
                Tab('Basic',
                    'title',
                    ),
                Tab('Advanced',
                    'override_url',
                    ),
            )
        )
