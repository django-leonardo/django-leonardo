# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin

from webcms.models import webcms_admin
from models import AnnotatedImage, ImageAnnotation, ImageAnnotationTranslation

admin.site.register(AnnotatedImage)
webcms_admin.register(AnnotatedImage)

class ImageAnnotationTranslation_Inline(admin.StackedInline):
    model = ImageAnnotationTranslation
    max_num = len(settings.LANGUAGES)

class ImageAnnotationAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'image', 'number', 'position', 'top', 'left', 'width', 'height', 'active',]
    list_filter = ['active', 'image', 'author', ]
    inlines = [ImageAnnotationTranslation_Inline, ]

admin.site.register(ImageAnnotation, ImageAnnotationAdmin)
webcms_admin.register(ImageAnnotation, ImageAnnotationAdmin)
