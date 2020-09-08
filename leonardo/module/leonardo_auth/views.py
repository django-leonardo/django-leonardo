
from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.contrib.sites.models import Site
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from leonardo import forms, messages

from .forms import (ChangePasswordForm, LoginForm, ResetPasswordForm,
                    ResetPasswordKeyForm, SignupForm, UserTokenForm)
from django.http import HttpResponseRedirect
from leonardo.decorators import require_auth

from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator


class HelperMixin(object):

    redirect_field_name = "next"

    success_url = getattr(settings, 'LOGIN_REDIRECT_URL', '/')

    @property
    def redirect_field_value(self):
        redirect_field_value = self.get_request_param(
            self.redirect_field_name)
        return redirect_field_value or self.success_url

    def get_success_url(self):
        return self.redirect_field_value

    def get_request_param(self, param, default=None):
        return self.request.POST.get(param) or self.request.GET.get(
            param, default)


class AuthViewMixin(HelperMixin):

    def dispatch(self, request, *args, **kwargs):
        # WORKAROUND: https://code.djangoproject.com/ticket/19316
        self.request = request
        # (end WORKAROUND)
        if request.user.is_authenticated() and \
                settings.LOGIN_REDIRECT_URL:
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        else:
            response = super(AuthViewMixin,
                             self).dispatch(request,
                                            *args,
                                            **kwargs)
        return response


class LoginView(AuthViewMixin, forms.ModalFormView):
    form_class = LoginForm
    template_name = 'leonardo_auth/login.html'
    success_url = getattr(settings, 'LOGIN_REDIRECT_URL', '/')
    submit_label = _("Login")

    def get_context_data(self, **kwargs):
        ret = super(LoginView, self).get_context_data(**kwargs)

        ret.update({
            "url": self.request.build_absolute_uri(),
            "view_name": _("Login"),
            "modal_size": 'sm',
            "site": Site.objects.get_current(),
            "redirect_field_name": self.redirect_field_name,
            "redirect_field_value": self.redirect_field_value,
            "modal_header": _("Login")})

        return ret

    def get_initial(self):
        return {}


class SignupView(AuthViewMixin, forms.ModalFormView):
    template_name = "leonardo/common/modal.html"
    form_class = SignupForm
    success_url = getattr(settings, 'LOGIN_REDIRECT_URL', '/')
    submit_label = _("Sign Up")

    def get_context_data(self, **kwargs):
        ret = super(SignupView, self).get_context_data(**kwargs)
        ret.update({
            "url": self.request.build_absolute_uri(),
            "view_name": _("Register"),
            "redirect_field_name": self.redirect_field_name,
            "redirect_field_value": self.redirect_field_value,
            "modal_header": _("Sign Up")})
        return ret


class ResetPasswordInitialView(AuthViewMixin, forms.ModalFormView):
    template_name = "leonardo/common/modal.html"
    form_class = ResetPasswordForm
    submit_label = _("Reset Password")

    def get_context_data(self, **kwargs):
        ret = super(ResetPasswordInitialView, self).get_context_data(**kwargs)
        ret.update({
            "url": self.request.build_absolute_uri(),
            "view_name": _("Register"),
            "redirect_field_name": self.redirect_field_name,
            "redirect_field_value": self.redirect_field_value,
            "modal_header": _("Reset password")})
        return ret


class ResetPasswordKeyView(AuthViewMixin, forms.ModalFormView):
    form_class = ResetPasswordKeyForm
    submit_label = _("Reset Password")

    def get_context_data(self, **kwargs):
        ret = super(ResetPasswordKeyView, self).get_context_data(**kwargs)
        ret.update({
            "url": self.request.build_absolute_uri(),
            "view_name": _("Register"),
            "redirect_field_name": self.redirect_field_name,
            "redirect_field_value": self.redirect_field_value,
            "modal_header": _("Sign Up")})
        return ret

    def dispatch(self, request, uidb36, key, **kwargs):
        self.request = request
        self.key = key
        # (Ab)using forms here to be able to handle errors in XHR #890
        token_form = UserTokenForm(data={'uidb36': uidb36, 'key': key})

        if not token_form.is_valid():
            self.reset_user = None
            messages.error(
                self.request, _('Token is invalid !'))
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        else:
            self.reset_user = token_form.reset_user
            return super(ResetPasswordKeyView, self).dispatch(request,
                                                              uidb36,
                                                              key,
                                                              **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ResetPasswordKeyView, self).get_form_kwargs()
        kwargs["user"] = self.reset_user
        kwargs["temp_key"] = self.key
        return kwargs


class ChangePasswordView(AuthViewMixin, forms.ModalFormView):
    form_class = ChangePasswordForm
    template_name = "leonrdo/common/modal.html"
    submit_label = _("Change Password")

    def get_context_data(self, **kwargs):
        ret = super(SignupView, self).get_context_data(**kwargs)
        ret.update({
            "url": self.request.build_absolute_uri(),
            "view_name": _("Register"),
            "redirect_field_name": self.redirect_field_name,
            "redirect_field_value": self.redirect_field_value,
            "modal_header": _("Change password")})
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
        ctx.update({
            "redirect_field_name": self.redirect_field_name,
            "redirect_field_value": self.redirect_field_value,
            "modal_header": _("Logout")})
        return ctx

    def get_redirect_url(self):
        ret = self.request.GET.get(
            self.redirect_field_name, settings.LOGOUT_URL)
        return ret


class PasswordChangeView(HelperMixin, forms.ModalFormView):
    template_name = 'leonardo_auth/change_password.html'
    form_class = ChangePasswordForm
    submit_label = _("Change Password")

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    @method_decorator(require_auth)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_usable_password():
            return HttpResponseRedirect(reverse('account_set_password'))
        return super(PasswordChangeView, self).dispatch(request, *args,
                                                        **kwargs)

    def get_context_data(self, **kwargs):
        ret = super(PasswordChangeView, self).get_context_data(**kwargs)
        # NOTE: For backwards compatibility
        ret['password_change_form'] = ret.get('form')
        ret.update({"modal_header": _("Change password")})
        # (end NOTE)
        return ret
