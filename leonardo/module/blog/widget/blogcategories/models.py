# -#- coding: utf-8 -#-

from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from elephantblog.models import Category
from leonardo.module.web.models import Widget


class BlogCategoriesWidget(Widget):

    def get_categories(self):
        return Category.objects.all()

    class Meta:
        abstract = True
        verbose_name = _("blog categories")
        verbose_name_plural = _("blog categories")
