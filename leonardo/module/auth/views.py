
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy

from django.conf import settings
from horizon import tables
from horizon import exceptions
from horizon import forms
from horizon import tabs
from horizon import workflows
from horizon import messages

from .forms import LoginForm

from django.contrib.sites.models import Site

from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect


class LoginView(forms.ModalFormView):
    form_class = LoginForm
    template_name = 'auth/login.html'
    success_url = reverse_lazy('horizon:user_home')

    redirect_field_name = "next"

    def get_context_data(self, **kwargs):
        ret = super(LoginView, self).get_context_data(**kwargs)
        redirect_field_value = self.request.REQUEST \
            .get(self.redirect_field_name)
        ret.update({
                    "site": Site.objects.get_current(),
                    "redirect_field_name": self.redirect_field_name,
                    "redirect_field_value": redirect_field_value})
        return ret

    def get_initial(self):
        return {}

"""
class SignupView(forms.ModalFormView):
    template_name = "module/auth/signup.html"
    form_class = SignupForm
    redirect_field_name = "next"
    success_url = None

    def get_success_url(self):
        # Explicitly passed ?next= URL takes precedence
        ret = (get_next_redirect_url(self.request,
                                     self.redirect_field_name)
               or self.success_url)
        return ret

    def form_valid(self, form):
        user = form.save(self.request)
        return complete_signup(self.request, user,
                               app_settings.EMAIL_VERIFICATION,
                               self.get_success_url())

    def get_context_data(self, **kwargs):
        form = kwargs['form']
        form.fields["email"].initial = self.request.session \
            .get('account_verified_email', None)
        ret = super(SignupView, self).get_context_data(**kwargs)
        login_url = passthrough_next_redirect_url(self.request,
                                                  reverse("account_login"),
                                                  self.redirect_field_name)
        redirect_field_name = self.redirect_field_name
        redirect_field_value = self.request.REQUEST.get(redirect_field_name)
        ret.update({"login_url": login_url,
                    "redirect_field_name": redirect_field_name,
                    "redirect_field_value": redirect_field_value})
        return ret
"""


class LogoutView(forms.ModalFormView):

    template_name = "account/logout.html"
    redirect_field_name = "next"

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, *args, **kwargs):
        url = self.get_redirect_url()
        if self.request.user.is_authenticated():
            self.logout()
        return redirect(url)

    def logout(self):
        messages.success(self.request, 'account/messages/logged_out.txt')
        auth_logout(self.request)

    def get_context_data(self, **kwargs):
        ctx = kwargs
        redirect_field_value = self.request.REQUEST \
            .get(self.redirect_field_name)
        ctx.update({
            "redirect_field_name": self.redirect_field_name,
            "redirect_field_value": redirect_field_value})
        return ctx

    def get_redirect_url(self):
        return settings.LOGOUT_URL
