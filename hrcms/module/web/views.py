from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django.views.generic.simple import direct_to_template

from feincms.module.page.models import Page

def page_xml_list(request, object_id=None):
    if object_id == None:
        object_list = Page.objects.filter(parent=None)
    else:
        obj = Page.objects.get(pk=object_id)
        object_list = Page.objects.filter(parent=obj)

    data = render_to_string('web/page_list.xml', {
        'object_list': object_list,
        'request': request,
    })

    response = HttpResponse(data, mimetype='text/xml')
    return response

def page_xml_detail(request, object_id):
    obj = Page.objects.get(pk=object_id)

    data = render_to_string('web/page_detail.xml', {
        'object': obj,
        'request': request,
    })
    
    response = HttpResponse(data, mimetype='text/xml')
    return response

def page_print_detail(request, object_id):
    object = Page.objects.get(id=object_id)
    return direct_to_template(request,
        template = 'web/page_print_detail.html',
        extra_context = {
            'object': object,
        }
    )
