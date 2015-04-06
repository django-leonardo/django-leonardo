# -*- coding: UTF-8 -*-

import datetime
import os
import glob

from django import forms
from django.db import models

from django.conf import settings
from django.core import urlresolvers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, RequestContext, loader
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _, ugettext as __
from django.utils.encoding import smart_str
from django.views.generic.simple import direct_to_template
from django.contrib.admin.views.decorators import staff_member_required

class FileForm(forms.Form):
    content = forms.CharField(label=_("File content"))

@staff_member_required
def css_edit(request, file_name):
    theme_root = os.path.join(settings.ENV_ROOT, 'sites', settings.SITE_NAME, 'project', 'assets')
    css1 = glob.glob('%s/*' % theme_root)
    css2 = glob.glob('%s/colors/*' % theme_root)
    css = css1 + css2
    parsed_css = []
    name = u''
    content = u''
    for raw_css in css:
        if os.path.isfile(raw_css):
            if raw_css.endswith('.css'):
                raw_file_name = raw_css.replace(u'%s/' %theme_root, '')
                file_handler = open(raw_css, "r")
                if raw_file_name == file_name:
                    name = raw_file_name
                    content = file_handler.read()
                parsed_css.append({
                    'name': raw_file_name,
                })
 
    if request.method == "POST":
        form = FileForm(request.POST)
        if form.is_valid():
            new_data = form.cleaned_data
    else:
        initial_data = {}
        form = FileForm()

    return render_to_response('theme/css_editor.html', {
        'form': form,
        'content': content,
        'file_name': file_name,
        'parsed_css': parsed_css, 
    },
    RequestContext(request))

@staff_member_required
def theme_home(request):

    return render_to_response('theme/theme_home.html', {
    },
    RequestContext(request))

@staff_member_required
def css_list(request):
    theme_root = os.path.join(settings.ENV_ROOT, 'sites', settings.SITE_NAME, 'project', 'assets')
    css1 = glob.glob('%s/*' % theme_root)
    css2 = glob.glob('%s/colors/*' % theme_root)
    css = css1 + css2
    parsed_css = []
    for raw_css in css:
        if os.path.isfile(raw_css):
            if raw_css.endswith('.css'):
                file_name = raw_css.replace(u'%s/' %theme_root, '')
                file_handler = open(raw_css, "r")
                file_content = file_handler.read()
                parsed_css.append({
                    'name': file_name,
                    'content': file_content,
                })
    return render_to_response('theme/css_list.html', {
        'parsed_css': parsed_css,
    },
    RequestContext(request))
