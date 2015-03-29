# -*- coding: UTF-8 -*-

import datetime
import os
import glob

from django import forms
from django.db import models

from django.contrib.auth.models import User, Group
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

@staff_member_required
def user_perms(request):
    staff = User.objects.filter(is_staff=True, is_superuser=False)
    managers = User.objects.filter(is_staff=True, is_superuser=True)
    groups = Group.objects.all()
    return render_to_response('auth/user_perms.html', {
        'groups': groups,
        'staff': staff,
        'managers': managers
    },
    RequestContext(request))

