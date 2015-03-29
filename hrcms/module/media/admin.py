# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin

from webcms.models import webcms_admin
from webcms.module.media.models import Category, CategoryAdmin, File, FileAdmin

admin.site.register(Category, CategoryAdmin)
webcms_admin.register(Category, CategoryAdmin)

admin.site.register(File, FileAdmin)
webcms_admin.register(File, FileAdmin)
