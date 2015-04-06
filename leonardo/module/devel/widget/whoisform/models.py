# -#- coding: utf-8 -#-

import pywhois

from django import forms

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.template import RequestContext

from webcms.models import Widget
from webcms.module.devel.widget.whoisform.forms import WhoisForm

from webcms.utils.models import MultiSelectField

SERVICE_CHOICES = (
    ('cz', _('.cz')),
    ('eu', _('.eu')),
    ('sk', _('.sk')),
    ('com', _('.com')),
    ('net', _('.net')),
    ('org', _('.org')),
    ('info', _('.info')),
    ('biz', _('.biz')),
    ('mobi', _('.mobi')),
    ('name', _('.name')),
)

class WhoisFormWidget(Widget):
    form = None
    search_multi = models.BooleanField(verbose_name=_('search multiple domains?'), default=False)
    tlds = MultiSelectField(max_length=255, blank=True, verbose_name=_('top level domains'), choices=SERVICE_CHOICES)

    class Meta:
        abstract = True
        verbose_name = _('whois form')
        verbose_name_plural = _('whois forms')

    @classmethod
    def initialize_type(cls, form=None):
        if form:
            cls.form = form

    def render_content(self, options):

        request = options.pop('request')
        result = ''

        if request.method == 'POST':
            form = WhoisForm(request.POST)

            if form.is_valid():
                if self.search_multi:
                    result = []
                    for tld in self.tlds:
                        status = True
                        try:
                            data = pywhois.whois('%s.%s' % (form.cleaned_data['domain'], tld))
                            if len(data.emails) > 0:
                                status = False
                        except:
                            data = None
                        result.append({
                            'tld': tld,
                            'name': form.cleaned_data['domain'],
                            'data': data,
                            'status': status,
                        })

                    return render_to_string(self.template_name, {
                        'widget': self,
                        'result': result,
                        'form': form,
                        'request': request,
                    }, context_instance=RequestContext(request))

                else:
                    result = pywhois.whois(form.cleaned_data['domain'])
                    return render_to_string(self.template_name, {
                        'widget': self,
                        'result': result,
                        'form': form,
                        'request': request,
                    }, context_instance=RequestContext(request))
        else:
            form = WhoisForm()

        return render_to_string(self.template_name, {
            'widget': self,
            'form': form,
        }, context_instance=RequestContext(request))

