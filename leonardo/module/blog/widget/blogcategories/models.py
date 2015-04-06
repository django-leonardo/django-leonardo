# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from hrcms.models import Widget

from elephantblog.models import Category

class BlogCategoriesWidget(Widget):

    def get_categories(self):
        return Category.objects.all()

    class Meta:
        abstract = True
        verbose_name = _("blog categories")
        verbose_name_plural = _("blog categories")
