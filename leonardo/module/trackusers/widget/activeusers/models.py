# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from webcms.models import Widget

SCOPE_CHOICES = (
    ('page', _("single page")),
    ('site', _("whole site")),
)

class ActiveUsersWidget(Widget):
    scope = models.CharField(max_length=255, verbose_name=_("scope"), choices=SCOPE_CHOICES, default="page")

    class Meta:
        abstract = True
        verbose_name = _("active users")
        verbose_name_plural = _('active users')
