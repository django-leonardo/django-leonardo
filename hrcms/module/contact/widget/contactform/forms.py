# -*- coding: UTF-8 -*-

import re
from random import randint

from django import forms
from django.utils.translation import ugettext_lazy as _

class MathCaptchaForm(forms.Form):

    Q_RE = re.compile("^(\d)\+(\d)$")
    A_RE = re.compile("^(\d+)$")

    captcha_question = forms.CharField(max_length=10, required=True, widget=forms.HiddenInput())
    captcha_answer = forms.CharField(max_length=2, label=_("answer"), required=True, widget = forms.TextInput(attrs={'size':'2'}))

    def __init__(self, *args, **kwargs):
        super(MathCaptchaForm, self).__init__(*args, **kwargs)
        q = self.data.get('captcha_question') or self._generate_question()
        self.initial['captcha_question'] = q

    def _generate_question(self):
        return "%s+%s" % (randint(1,9), randint(1,9))

    def clean_captcha_answer(self):
        q = self.Q_RE.match(self.cleaned_data['captcha_question'])

        if not q:
            raise forms.ValidationError(_("Are you hacker?"))

        q = q.groups()

        a = self.A_RE.match(self.cleaned_data['captcha_answer'])

        if not a:
            raise forms.ValidationError(_("Number is expected!"))

        a = a.groups()

        if int(q[0]) + int(q[1]) != int(a[0]):
            raise forms.ValidationError(_("Are you human?"))

class HoneypotCaptchaForm(forms.Form):
    body = forms.CharField(max_length=10, required=False)

    def clean_body(self):
        if self.cleaned_data['body'] != "":
            raise forms.ValidationError(_("Are you human?"))

class ContactForm(forms.Form):
    name = forms.CharField(label=_('contact name'))
    email = forms.EmailField(label=_('contact email'))
    phone = forms.CharField(label=_('contact phone'), required=False, max_length=50,)
    website = forms.URLField(label=_('contact website'), required=False)
    subject = forms.CharField(label=_('contact subject'), required=False)

    content = forms.CharField(widget=forms.Textarea, required=True, label=_('contact message'))
