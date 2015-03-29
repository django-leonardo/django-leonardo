# -#- coding: utf-8 -#-

from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from uni_form.helpers import FormHelper, Submit, Reset

from uni_form.helpers import Layout, Fieldset, Column, Row, HTML

from webcms.models import Widget

TEST_CHOICES = (
    ('para', _("paragraphs")),
    ('list', _("lists")),
    ('heading', _("headings")),
    ('table', _("tables")),
    ('form', _("forms")),
    ('states', _("states")),
    ('content', _("content")),
    ('misc', _("misc")),
)

class VisualTestModel(models.Model):
    datetime_simple = models.DateTimeField(verbose_name=_("Date taken"), blank=True, null=True, default='para')

    class Meta:
        abstract = True

CHOICES = (
            ("A", "Alpha"),
            ("B", "Bravo"),
            ("C", "Charlie"),                        
        )

class VisualTestForm(forms.ModelForm):
    character_field = forms.CharField(label="Character Field", help_text="I am help text", max_length=30, required=True, widget=forms.TextInput())
    url_field = forms.URLField(label='URL field', verify_exists=False, max_length=100, required=True, widget=forms.TextInput())
    textarea_field = forms.CharField(label='Textareafield', required=True, widget=forms.Textarea())
#    hidden_field = forms.CharField(label='textarea_field', required=True, widget=forms.HiddenInput())
    file_field  = forms.FileField(label="File Field",required=False)
    password_field_1 = forms.CharField(label='Password field', max_length=100, widget=forms.PasswordInput())
    password_field_2 = forms.CharField(label='Password field', max_length=100, widget=forms.PasswordInput())

    boolean_field = forms.BooleanField(label="Boolean Field", required=False)
    choice_field = forms.ChoiceField(label="Choice Field", required=False, choices=CHOICES)
    multiple_choice_field = forms.MultipleChoiceField(label="multiple_choice_field", required=False, choices=CHOICES)

    helper = FormHelper()
    
    # Add in a class and id
    helper.form_id = 'this-form-rocks'
    helper.form_class = 'search'
    
    # add in a submit and reset button
    submit = Submit('enter','enter some data')
    helper.add_input(submit)
    reset = Reset('reset','reset button')
    helper.add_input(reset)

    layout = Layout(
        Fieldset('',
            Row('character_field', 'url_field'),
        ),
        Fieldset(_('Contact details'),
            Row('password_field_1','password_field_2'),
            'boolean_field',
            'choice_field',
        )
    )

    helper.add_layout(layout)

    class Meta:
        model = VisualTestModel

class VisualTestWidget(Widget):
    test = models.CharField(max_length=255, verbose_name=_("type of test"), choices=TEST_CHOICES, default="general")

    def test_page(self):
        return "widget/visualtest/test_%s.html" % self.test

    class Meta:
        abstract = True
        verbose_name = _("visual tester")
        verbose_name_plural = _('visual testers')

    def render_content(self, options):
        if self.test == 'form':
            form = VisualTestForm()
        else:
            form = None

        return render_to_string(self.template_name, { 
            'widget': self,
            'request': options['request'],
            'form': form
        })
