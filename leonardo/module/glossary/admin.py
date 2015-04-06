# -#- coding: utf-8 -#-

from django.contrib import admin
from django.conf import settings
from django.db import models

from django.utils.translation import get_language, ugettext_lazy as _

from webcms.module.glossary.models import Term, TermTranslation
from webcms.models import webcms_admin

class TermTranslation_Inline(admin.StackedInline):
    model = TermTranslation
    max_num = len(settings.LANGUAGES)
    prepopulated_fields = {"slug": ("name",)}

def tagline(object):
    return object.translation.excerpt

class TermAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'synonym', tagline, 'active', ]
    list_filter = ['active', 'synonym']
    list_per_page = 50
    inlines = [TermTranslation_Inline,]

admin.site.register(Term, TermAdmin)
webcms_admin.register(Term, TermAdmin)
