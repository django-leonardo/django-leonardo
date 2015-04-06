# -#- coding: utf-8 -#-

from django import forms
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.template.context import RequestContext
from django.utils.safestring import mark_safe

from webcms.models import Widget
from webcms.module.contact.widget.contactform.forms import MathCaptchaForm, HoneypotCaptchaForm, ContactForm

class MathCaptchaContactForm(ContactForm, MathCaptchaForm):

    def __init__(self, *args, **kwargs):
        super(MathCaptchaContactForm, self).__init__(*args, **kwargs)

class HoneypotCaptchaContactForm(ContactForm, HoneypotCaptchaForm):

    def __init__(self, *args, **kwargs):
        super(HoneypotCaptchaContactForm, self).__init__(*args, **kwargs)
        self.fields['content'].required = True

CAPTCHA_CHOICES = (
    ('math', _('Mathematical catchpa')),
    ('honeypot', _('Honeypot catchpa')),
#    ('akismet', 'Akismet'),
)

class ContactFormWidget(Widget):
    form = None

    email = models.EmailField()
    subject = models.CharField(max_length=200, verbose_name=_("form subject"))
    captcha = models.CharField(max_length=20, verbose_name=_("protection"), choices=CAPTCHA_CHOICES, default="math")

    class Meta:
        abstract = True
        verbose_name = _('contact form')
        verbose_name_plural = _('contact forms')

    @classmethod
    def initialize_type(cls, form=None):
        if form:
            cls.form = form

    def render_content(self, options):

        request = options.pop('request')

        if request.method == 'POST':
            if self.captcha == 'math':
                form = MathCaptchaContactForm(request.POST)
            if self.captcha == 'honeypot':
                form = HoneypotCaptchaContactForm(request.POST)

            if form.is_valid():
                emails = self.email.split(';')
                send_mail(
                    u'%s %s' % (settings.EMAIL_SUBJECT_PREFIX, _('Message from contact form')),
                    render_to_string('email/contact_notice.txt', {
                        'data': form.cleaned_data,
                    }),
                    settings.DEFAULT_FROM_EMAIL,
                    emails,
                    fail_silently=False)

                context = RequestContext(request, {
                    'widget': self,
                    'request': request,
                    'sent': True,
                })

                return render_to_string(self.template_name, context)

        else:
            initial = {'subject': self.subject }
            if request.user.is_authenticated():
                initial['email'] = request.user.email
                initial['name'] = request.user.get_full_name()
            if self.captcha == 'math':
                form = MathCaptchaContactForm(initial=initial)
            if self.captcha == 'honeypot':
                form = HoneypotCaptchaContactForm(initial=initial)

        context = RequestContext(request, {
            'widget': self,
            'form': form,
        })

        return render_to_string(self.template_name, context)
