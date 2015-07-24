# -#- coding: utf-8 -#-

from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from leonardo import messages
from leonardo.fields import MultiSelectField
from leonardo.module.web.models import Widget

from .utils import add_client_type, get_client_ip

INFO_CHOICES = (
    ('browser', _('browser information')),
    ('os', _('operating system')),
    ('ip', _('IP address')),
    ('hostname', _('hostname')),
)


class ClientInfoWidget(Widget):

    show_info = MultiSelectField(
        max_length=255, default='browser', verbose_name=_("show info"), choices=INFO_CHOICES)

    class Meta:
        abstract = True
        verbose_name = _("client info")
        verbose_name_plural = _('client info')

    def render_content(self, options):
        request = options.get('request')
        uas = None
        user_agent = ''
        ip = get_client_ip(request)
        host = request.get_host()
        if 'browser' in self.show_info or 'os' in self.show_info:
            try:
                import httpagentparser
            except ImportError:
                messages.error(request, _('Please install httpagentparser'))
            else:
                uas = request.META.get('HTTP_USER_AGENT')
                user_agent = httpagentparser.detect(uas)
        request = add_client_type(request)
        context = RequestContext(request, {
            'user_agent': user_agent,
            'ip': ip,
            'host': host,
            'widget': self,
        })
        return render_to_string(self.get_template, context)
