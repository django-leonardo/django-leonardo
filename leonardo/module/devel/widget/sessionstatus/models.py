# -#- coding: utf-8 -#-

from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.template import RequestContext

from webcms.models import Widget

VERBOSITY_CHOICES = (
    ('brief', _("brief")),
    ('full', _("full")),
)

class SessionStatusWidget(Widget):
    verbosity = models.CharField(max_length=255, verbose_name=_("verbosity level"), choices=VERBOSITY_CHOICES, default="full")

    def render_content(self, options):
        request = options.get('request')

        try:
            fragments = request._feincms_fragments
        except:
            fragments = {}
        context = RequestContext(request, { 
            'fragments': fragments,
            'widget': self,
        })
        return render_to_string(self.template_name, context)

    class Meta:
        abstract = True
        verbose_name = _("session status")
        verbose_name_plural = _('session statuses')
