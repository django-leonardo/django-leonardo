# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin

from .models import Category, CategoryAdmin, File, FileAdmin

admin.site.register(Category, CategoryAdmin)

admin.site.register(File, FileAdmin)
