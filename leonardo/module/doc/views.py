# -*- coding: UTF-8 -*-

import trml2pdf

from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.template import loader, RequestContext
from django.http import HttpResponse
from django.utils.encoding import smart_unicode, smart_str
from django.contrib.auth.decorators import login_required 

from feincms.views.decorators import standalone

from models import Document

@login_required
def document_list(request):
    object_list = Document.objects.order_by('-published_on')
    return direct_to_template(request,
        template = 'doc/document_list.html',
        extra_context = {
            'object_list': object_list,
        }
    )

@login_required
def document_detail(request, object_id, format='html'):
    object = Document.objects.get(pk=object_id)
    object_list = Document.objects.order_by('-published_on')
    return direct_to_template(request,
        template = 'doc/document_detail.html',
        extra_context = {
            'object': object,
            'format': format,
            'object_list': object_list,
        }
    )

@login_required
@standalone
def document_file(request, object_id, format):
    object = Document.objects.get(pk=object_id)
    context = RequestContext(request, {
        'object': object,
        'base_template': 'doc_base.%s' % format,
        'format': format,
    })
    string = loader.render_to_string('doc/document_file.html', context)

    if format == 'html':
        response = HttpResponse(mimetype='text/html')
        response.write(string)
    elif format == 'rml':
        output = trml2pdf.parseString(smart_str(string))
        #response = HttpResponse(mimetype='text/html')
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=file.pdf'
        response.write(output)

    return response