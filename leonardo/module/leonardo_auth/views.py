
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model
from django.conf import settings
from leonardo import forms
from leonardo import messages

from .forms import LoginForm, SignupForm, ChangePasswordForm, ResetPasswordForm, ResetPasswordKeyForm

from django.contrib.sites.models import Site

from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect

from django.views.decorators.debug import sensitive_post_parameters  # noqa


class LoginView(forms.ModalFormView):
    form_class = LoginForm
    template_name = 'leonardo_auth/login.html'
    success_url = getattr(settings, 'LOGIN_REDIRECT_URL', '/')

    redirect_field_name = "next"

    def get_success_url(self):
        # Explicitly passed ?next= URL takes precedence
        ret = self.request.GET.get(self.redirect_field_name, self.success_url)
        return ret

    def get_context_data(self, **kwargs):
        ret = super(LoginView, self).get_context_data(**kwargs)
        redirect_field_value = self.request.GET \
            .get(self.redirect_field_name)
        ret.update({
            "url": self.request.build_absolute_uri(),
            "view_name": _("Login"),
            "modal_size": 'sm',
            "site": Site.objects.get_current(),
            "redirect_field_name": self.redirect_field_name,
            "redirect_field_value": redirect_field_value,
            "modal_header": _("Login")})
        return ret

    def get_initial(self):
        return {}


class SignupView(forms.ModalFormView):
    template_name = "leonardo/common/modal.html"
    form_class = SignupForm
    redirect_field_name = "next"
    success_url = getattr(settings, 'LOGIN_REDIRECT_URL', '/')

    def get_success_url(self):
        # Explicitly passed ?next= URL takes precedence
        ret = getattr(self.kwargs, self.redirect_field_name, self.success_url)
        return ret

    def get_context_data(self, **kwargs):
        ret = super(SignupView, self).get_context_data(**kwargs)
        redirect_field_name = self.redirect_field_name
        redirect_field_value = self.request.REQUEST.get(redirect_field_name)
        ret.update({
            "url": self.request.build_absolute_uri(),
            "view_name": _("Register"),
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": redirect_field_value,
            "modal_header": _("Sign Up")})
        return ret

class ResetPasswordInitialView(forms.ModalFormView):
    template_name = "leonardo/common/modal.html"
    form_class = ResetPasswordForm
    redirect_field_name = "next"

    def get_success_url(self):
        # Explicitly passed ?next= URL takes precedence
        ret = getattr(self.kwargs, self.redirect_field_name, self.success_url)
        return ret

    def get_context_data(self, **kwargs):
        ret = super(ResetPasswordInitialView, self).get_context_data(**kwargs)
        redirect_field_name = self.redirect_field_name
        redirect_field_value = self.request.REQUEST.get(redirect_field_name)
        ret.update({
            "url": self.request.build_absolute_uri(),
            "view_name": _("Register"),
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": redirect_field_value,
            "modal_header": _("Sign Up")})
        return ret


class ResetPasswordKeyView(forms.ModalFormView):
    form_class = ResetPasswordKeyForm
    redirect_field_name = "next"

    def get_success_url(self):
        # Explicitly passed ?next= URL takes precedence
        ret = getattr(self.kwargs, self.redirect_field_name, self.success_url)
        return ret

    def get_context_data(self, **kwargs):
        ret = super(ResetPasswordKeyView, self).get_context_data(**kwargs)
        redirect_field_name = self.redirect_field_name
        redirect_field_value = self.request.REQUEST.get(redirect_field_name)
        ret.update({
            "url": self.request.build_absolute_uri(),
            "view_name": _("Register"),
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": redirect_field_value,
            "modal_header": _("Sign Up")})
        return ret

    def dispatch(self, request, uidb36, key, **kwargs):
        self.request = request
        self.key = key
        # (Ab)using forms here to be able to handle errors in XHR #890
        token_form = UserTokenForm(data={'uidb36': uidb36, 'key': key})

        if not token_form.is_valid():
            self.reset_user = None
            response = self.render_to_response(
                self.get_context_data(token_fail=True)
            )
            return _ajax_response(self.request, response, form=token_form)
        else:
            self.reset_user = token_form.reset_user
            return super(PasswordResetFromKeyView, self).dispatch(request,
                                                                  uidb36,
                                                                  key,
                                                                  **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PasswordResetFromKeyView, self).get_form_kwargs()
        kwargs["user"] = self.reset_user
        kwargs["temp_key"] = self.key
        return kwargs


class ChangePasswordView(forms.ModalFormView):
    form_class = ChangePasswordForm
    template_name = "leonrdo/common/modal.html"
    redirect_field_name = "next"

    def get_success_url(self):
        # Explicitly passed ?next= URL takes precedence
        ret = getattr(self.kwargs, self.redirect_field_name, self.success_url)
        return ret

    def get_context_data(self, **kwargs):
        ret = super(SignupView, self).get_context_data(**kwargs)
        redirect_field_name = self.redirect_field_name
        redirect_field_value = self.request.REQUEST.get(redirect_field_name)
        ret.update({
            "url": self.request.build_absolute_uri(),
            "view_name": _("Register"),
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": redirect_field_value,
            "modal_header": _("Sign Up")})
        return ret


class LogoutView(forms.ModalFormView):

    template_name = "leonrdo/common/modal.html"
    redirect_field_name = "next"

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, *args, **kwargs):
        url = self.get_redirect_url()
        if self.request.user.is_authenticated():
            self.logout()
        return redirect(url)

    def logout(self):
        messages.success(self.request, _('Logout complete'))
        auth_logout(self.request)

        self.request.session.flush()
        if hasattr(self.request, 'user'):
            from django.contrib.auth.models import AnonymousUser
            self.request.user = AnonymousUser()

    def get_context_data(self, **kwargs):
        ctx = kwargs
        redirect_field_value = self.request.REQUEST \
            .get(self.redirect_field_name)
        ctx.update({
            "redirect_field_name": self.redirect_field_name,
            "redirect_field_value": redirect_field_value,
            "modal_header": _("Logout")})
        return ctx

    def get_redirect_url(self):
        ret = self.request.GET.get(
            self.redirect_field_name, settings.LOGOUT_URL)
        return ret

