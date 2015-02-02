
import os

from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.models import User, Group

from . import views

urlpatterns = patterns('',
    
    url(r'$', views.PortalView.as_view(), name='index'),

)