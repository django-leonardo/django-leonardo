# -*- coding: UTF-8 -*-

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import get_language_from_request
from django.views.generic.list_detail import object_list, object_detail
from django.core.mail import mail_managers
from django import forms

from feincms.module.page.models import Page

from webcms.module.folio.models import Service, ProjectTranslation, Project, Client, Category, CategoryTranslation

def project_list(request):
    category_list = Category.objects.filter(active=True, parent=None)
    client_list = Client.objects.filter(active=True)
    object_list = Project.objects.filter(active=True)
    context = RequestContext(request, {
        'object_list': object_list,
        'client_list': client_list,
        'xx': 'xxxxxx',
        'category_list': category_list,
    })
    return render_to_response('folio/project_list.html', {}, context_instance=context)

def category_detail(request, client_slug=None):
    category_list = Category.objects.all()
    category = CategoryTranslation.objects.get(slug=category_slug).parent
    object = ProjectTranslation.objects.get(slug=project_slug, parent__category=category).parent
    return render_to_response(
        'folio/project_detail.html', {
            'object': object,
            'category': category,
        },
        context_instance=RequestContext(request)
    )

def client_detail(request, client_slug=None):
    category_list = Category.objects.all()
    category = CategoryTranslation.objects.get(slug=category_slug).parent
    object = ProjectTranslation.objects.get(slug=project_slug, parent__category=category).parent
    return render_to_response(
        'folio/project_detail.html', {
            'object': object,
            'category': category,
        },
        context_instance=RequestContext(request)
    )

def project_detail(request, project_slug=None):
    category_list = Category.objects.all()
    object = ProjectTranslation.objects.get(slug=project_slug).parent
    return render_to_response(
        'folio/project_detail.html', {
            'object': object,
        },
        context_instance=RequestContext(request)
    )

# projects by category app

def project_category_list(request, category_slug=None):
    category_list = Category.objects.all()
    if category_slug == None:
        category = None
        object_list = Project.objects.filter(active=True, featured=True)
    else:
        category = CategoryTranslation.objects.get(slug=category_slug).parent
        object_list = Project.objects.filter(active=True, categories=category)
    return render_to_response(
        'folio/project_list.html', {
            'object_list': object_list,
            'category': category,
            'category_list': category_list,
            'xx': 'xxxxxx',
        },
        context_instance=RequestContext(request)
    )

def project_category_detail(request, category_slug=None, project_slug=None):
    lang = get_language_from_request(request)
    category_list = Category.objects.all()
    category = CategoryTranslation.objects.get(slug=category_slug).parent
    object = ProjectTranslation.objects.get(slug=project_slug, parent__categories=category, language_code__exact=lang).parent
    object_list = Project.objects.filter(categories=category)
    i = 0
    for proj in object_list:
        if proj.id == object.id:
            if i > 0:
                prev = object_list[i-1]
            else:
                prev = None
            if i < (object_list.count() - 1):
                next = object_list[i+1]
            else:
                next = None
        i += 1

    return render_to_response(
        'folio/project_detail.html', {
            'object': object,
            'prev': prev,
            'next': next,
            'category': category,
        },
        context_instance=RequestContext(request)
    )

def project_list_client(request, client_uri=None):
    service_list = Service.objects.order_by('sort_order')
    if service_uri == None:
        service = service_list[0]
    else:
        service = Service.objects.get(uri=service_uri)
    page = Page.objects.best_match_for_path(request.path, raise404=False)
    return render_to_response(
        'portfolio/project_list.html', {
            'object_list': Project.objects.filter(active=True, services=service),
            'service': service,
            'service_list': service_list,

            'page': page
        },
        context_instance=RequestContext(request)
    )
