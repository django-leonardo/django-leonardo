# -#- coding: utf-8 -#-

from django.contrib import admin
from django.conf import settings

from django.utils.translation import get_language, ugettext_lazy as _

from webcms.models import webcms_admin
from models import Faq, FaqCategory, FaqTranslation, FaqCategoryTranslation

class FaqTranslation_Inline(admin.TabularInline):
    model   = FaqTranslation
    max_num = len(settings.LANGUAGES)

class FaqAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'category', 'ordering', 'active' ]
    list_filter = ['category']
    list_per_page = 50
    inlines = [FaqTranslation_Inline,]

admin.site.register(Faq, FaqAdmin)
webcms_admin.register(Faq, FaqAdmin)

class Faq_Inline(admin.TabularInline):
    model = Faq

class FaqCategoryTranslation_Inline(admin.TabularInline):
    model   = FaqCategoryTranslation
    max_num = len(settings.LANGUAGES)

class FaqCategoryAdmin(admin.ModelAdmin):
    list_display = ['__unicode__' ]
    inlines = [Faq_Inline, FaqCategoryTranslation_Inline]

admin.site.register(FaqCategory, FaqCategoryAdmin)
webcms_admin.register(FaqCategory, FaqCategoryAdmin)
