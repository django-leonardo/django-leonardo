# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from leonardo.module.web.models import Widget


LOGIN_TYPE_CHOICES = (
    (1, _("Admin")),
    (2, _("Public")),
)


class UserLoginWidget(Widget):
    type = models.PositiveIntegerField(verbose_name=_(
        "type"), choices=LOGIN_TYPE_CHOICES, default=2)

    def get_context_data(self, request):

        context = super(UserLoginWidget, self).get_context_data(request)

        if 'next' in request.GET:
            context['next'] = request.GET['next']
        else:
            context['next'] = request.path

        return context

    class Meta:
        abstract = True
        verbose_name = _("user login")
        verbose_name_plural = _("user logins")
