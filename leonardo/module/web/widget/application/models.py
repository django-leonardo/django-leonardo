# -#- coding: utf-8 -#-

import re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.template import RequestContext

from leonardo.module.web.models import Widget
from feincms.content.application.models import ApplicationContent

class ApplicationWidget(Widget, ApplicationContent):

    def render_content(self, options):

        try:
            data = { 
                'widget': self,
                'content': self.rendered_result
            }
        except:
            data = { 
                'widget': self,
                'content': '<div class="alert">no rendered result</div>'
            }
        context = RequestContext(options.get('request'), data)

        return render_to_string(self.get_template, context)

    class Meta:
        abstract = True
        verbose_name = _("external application")
        verbose_name_plural = _('external applications')
