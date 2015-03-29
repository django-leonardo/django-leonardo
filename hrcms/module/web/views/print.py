from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django.views.generic.simple import direct_to_template

from feincms.module.page.models import Page

def page_print_detail(request, object_id):
    object = Page.objects.get(id=object_id)
    return direct_to_template(request,
        template = 'web/page_print_detail.html',
        extra_context = {
            'object': object,
        }
    )
