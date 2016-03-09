
from django.db import models
from django.utils.translation import ugettext_lazy as _
from leonardo.module.nav.forms import NavigationForm
from leonardo.module.web.models import Page, Widget


class SimpleLinkWidget(Widget):

    feincms_item_editor_form = NavigationForm
    page = models.ForeignKey(Page, verbose_name=_(
        "Linked page"), related_name="simplelink_node")

    class Meta:
        abstract = True
        verbose_name = _("Simple link")
        verbose_name_plural = _('Simple links')
