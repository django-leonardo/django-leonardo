# -#- coding: utf-8 -#-

from django.utils.translation import ugettext_lazy as _

from leonardo.module.web.models import Widget


class UserRegistrationWidget(Widget):

    def get_context_data(self, request):

        context = super(UserRegistrationWidget, self).get_context_data(request)

        if 'next' in request.GET:
            context['next'] = request.GET['next']

        return context

    class Meta:
        abstract = True
        verbose_name = _("user registration")
        verbose_name_plural = _("user registrations")
