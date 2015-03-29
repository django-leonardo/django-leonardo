# -*- coding: UTF-8 -*-

from datetime import date
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.template.loader import render_to_string
from django.http import HttpResponse

from django.http import Http404

from webcms.module.news.models import NewsEntry

def news_entry_list(request):
    object_list = NewsEntry.objects.filter(published=True).order_by('-published_on')
    return direct_to_template(request,
        template = 'news/news_entry_list.html',
        extra_context = {
            'object_list': object_list,
        }
    )

def news_entry_xml_list(request):
    object_list = NewsEntry.objects.filter(published=True).order_by('-published_on')
    template = 'news/news_entry_list.xml'
    data = render_to_string(template, {
        'object_list': object_list,
        'request': request,
    })
    response = HttpResponse(data, mimetype='text/xml')
    return response

def _get_entry_detail(request, object, template):
    object_list = NewsEntry.objects.filter(published=True).order_by('-published_on')
    i = 0
    j = 0
    tmp = []
    for entry in object_list:
        tmp.append(entry)
        if entry.id == object.id:
            j = i
        i = i + 1
    if j > 0:
        prev = tmp[j-1]
    else:
        prev = None
    if len(tmp) > 1 and j < len(tmp) - 1:
        next = tmp[j+1]
    else:
        next = None
    return render_to_string(template, {
        'request': request,
        'object': object,
        'prev': prev,
        'next': next
    })

def news_entry_detail(request, year, month, day, object_slug):
    if year == None:
        object = NewsEntry.objects.get(slug=object_slug)
    else:
        try:
            published_on = date(int(year), int(month), int(day))
        except ValueError:
            raise Http404

        object = get_object_or_404(Entry.objects.select_related(),
            published_on__year=published_on.year,
            published_on__month=published_on.month,
            published_on__day=published_on.day,
            slug=object_slug)

    template = 'news/news_entry_detail.html'
    data = _get_entry_detail(request, object, template)
    response = HttpResponse(data)
    return response

def news_entry_xml_detail(request, object_id):
    object = NewsEntry.objects.get(pk=object_id)
    template = 'news/news_entry_detail.xml'
    data = _get_entry_detail(request, object, template)
    response = HttpResponse(data, mimetype='text/xml')
    return response
