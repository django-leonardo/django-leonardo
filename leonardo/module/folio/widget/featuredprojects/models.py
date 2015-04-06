# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from webcms.models import Widget

from webcms.module.folio.models import Project

class FeaturedProjectsWidget(Widget):
    project_count = models.PositiveIntegerField(verbose_name=_("project count"), default=2)
    show_link = models.BooleanField(default=True, verbose_name=_("show link button"))

    def get_projects(self):
        return Project.objects.filter(active=True, featured=True)[:self.project_count]

    class Meta:
        abstract = True
        verbose_name = _("featured projects")
        verbose_name_plural = _("featured projects")
