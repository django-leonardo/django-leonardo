# -#- coding: utf-8 -#-

from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.template import RequestContext

from webcms.models import Widget
from webcms.utils.models import MultiSelectField

INFO_CHOICES = (
    ('browser', _('browser information')),
    ('os', _('operating system')),
    ('ip', _('IP address')),
    ('hostname', _('hostname')),
)

class ClientInfoWidget(Widget):
    show_info = MultiSelectField(max_length=255, default='browser', verbose_name=_("show info"), choices=INFO_CHOICES)

    class Meta:
        abstract = True
        verbose_name = _("client info")
        verbose_name_plural = _('client info')

    def render_content(self, options):
        request = options.get('request')
        uas = None
        user_agent = ''
        ip = request.META.get('REMOTE_ADDR')
        host = request.META.get('REMOTE_HOST')
        if 'browser' in self.show_info or 'os' in self.show_info:
            import httpagentparser
            uas = request.META.get('HTTP_USER_AGENT')
            user_agent = httpagentparser.detect(uas)
        context = RequestContext(request, { 
            'user_agent': user_agent,
            'ip': ip,
            'host': host,
            'widget': self,
        })
        return render_to_string(self.template_name, context)
