from __future__ import absolute_import

import warnings

from django import forms
from django.core.urlresolvers import reverse
from django.core import exceptions
from django.db.models import Q
from django.utils.translation import pgettext, ugettext_lazy as _, ugettext

from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site

from allauth.utils import (email_address_exists, get_user_model,
                     set_form_field_order,
                     build_absolute_uri)

from allauth.account.models import EmailAddress
from allauth.account.utils import (perform_login, setup_user_email, user_username,
                    user_pk_to_url_str)
from allauth.account.app_settings import AuthenticationMethod
from allauth.account import app_settings
from allauth.account.adapter import get_adapter

from horizon import forms as horizon_forms

from allauth.account.utils import (get_next_redirect_url, complete_signup,
                    get_login_redirect_url, perform_login,
                    passthrough_next_redirect_url,
                    url_str_to_user_pk)

from horizon import messages

try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module

class PasswordField(forms.CharField):

    def __init__(self, *args, **kwargs):
        render_value = kwargs.pop('render_value',
                                  app_settings.PASSWORD_INPUT_RENDER_VALUE)
        kwargs['widget'] = forms.PasswordInput(render_value=render_value,
                                               attrs={'placeholder':
                                                      _('Password')})
        super(PasswordField, self).__init__(*args, **kwargs)


class SetPasswordField(PasswordField):

    def clean(self, value):
        value = super(SetPasswordField, self).clean(value)
        value = get_adapter().clean_password(value)
        return value


class LoginForm(horizon_forms.SelfHandlingForm):

    password = PasswordField(label=_("Password"))
    remember = horizon_forms.BooleanField(label=_("Remember Me"),
                                  required=False)

    user = None
    error_messages = {
        'account_inactive':
        _("This account is currently inactive."),

        'email_password_mismatch':
        _("The e-mail address and/or password you specified are not correct."),

        'username_password_mismatch':
        _("The username and/or password you specified are not correct."),

        'username_email_password_mismatch':
        _("The login and/or password you specified are not correct.")
    }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        if app_settings.AUTHENTICATION_METHOD == AuthenticationMethod.EMAIL:
            login_widget = forms.TextInput(attrs={'type': 'email',
                                                  'placeholder':
                                                  _('E-mail address'),
                                                  'autofocus': 'autofocus'})
            login_field = forms.EmailField(label=_("E-mail"),
                                           widget=login_widget)
        elif app_settings.AUTHENTICATION_METHOD \
                == AuthenticationMethod.USERNAME:
            login_widget = forms.TextInput(attrs={'placeholder':
                                                  _('Username'),
                                                  'autofocus': 'autofocus'})
            login_field = forms.CharField(label=_("Username"),
                                          widget=login_widget,
                                          max_length=30)
        else:
            assert app_settings.AUTHENTICATION_METHOD \
                == AuthenticationMethod.USERNAME_EMAIL
            login_widget = forms.TextInput(attrs={'placeholder':
                                                  _('Username or e-mail'),
                                                  'autofocus': 'autofocus'})
            login_field = forms.CharField(label=pgettext("field label",
                                                         "Login"),
                                          widget=login_widget)
        self.fields["login"] = login_field
        set_form_field_order(self,  ["login", "password", "remember"])
        if app_settings.SESSION_REMEMBER is not None:
            del self.fields['remember']

    def user_credentials(self):
        """
        Provides the credentials required to authenticate the user for
        login.
        """
        credentials = {}
        login = self.cleaned_data["login"]
        if app_settings.AUTHENTICATION_METHOD == AuthenticationMethod.EMAIL:
            credentials["email"] = login
        elif (app_settings.AUTHENTICATION_METHOD
              == AuthenticationMethod.USERNAME):
            credentials["username"] = login
        else:
            if "@" in login and "." in login:
                credentials["email"] = login
            credentials["username"] = login
        credentials["password"] = self.cleaned_data["password"]
        return credentials

    def clean_login(self):
        login = self.cleaned_data['login']
        return login.strip()

    def clean(self):
        if self._errors:
            return
        user = authenticate(**self.user_credentials())
        if user:
            self.user = user
        else:
            raise forms.ValidationError(
                self.error_messages[
                    '%s_password_mismatch'
                    % app_settings.AUTHENTICATION_METHOD])
        return self.cleaned_data

    def login(self, request, redirect_url=None):
        ret = perform_login(request, self.user,
                            email_verification=app_settings.EMAIL_VERIFICATION,
                            redirect_url=redirect_url)
        remember = app_settings.SESSION_REMEMBER
        if remember is None:
            remember = self.cleaned_data['remember']
        if remember:
            request.session.set_expiry(app_settings.SESSION_COOKIE_AGE)
        else:
            request.session.set_expiry(0)
        return ret


    def handle(self, request, data):

        result = self.login(request)

        if request.user.is_authenticated():
            messages.success(request, "Login success.")
            return True
        messages.error(request, "Login failed.")
        return False

class SignupForm(horizon_forms.SelfHandlingForm):

    username = forms.CharField(label=_("Username"),
                               max_length=30,
                               min_length=app_settings.USERNAME_MIN_LENGTH,
                               widget=forms.TextInput(
                                   attrs={'placeholder':
                                          _('Username'),
                                          'autofocus': 'autofocus'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'type': 'email',
               'placeholder': _('E-mail address')}))

    password1 = SetPasswordField(label=_("Password"))
    password2 = PasswordField(label=_("Password (again)"))
    confirmation_key = forms.CharField(max_length=40,
                                       required=False,
                                       widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        if not app_settings.SIGNUP_PASSWORD_VERIFICATION:
            del self.fields["password2"]

    def clean(self):
        super(SignupForm, self).clean()
        if app_settings.SIGNUP_PASSWORD_VERIFICATION \
                and "password1" in self.cleaned_data \
                and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] \
                    != self.cleaned_data["password2"]:
                raise forms.ValidationError(_("You must type the same password"
                                              " each time."))
        return self.cleaned_data

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        adapter.save_user(request, user, self)
        #self.custom_signup(request, user)
        # TODO: Move into adapter `save_user` ?
        setup_user_email(request, user, [])
        return user
    
    def handle(self, request, data):

        user = self.save(self.request)
        return complete_signup(self.request, user,
                               app_settings.EMAIL_VERIFICATION,
                               self.get_success_url())

class UserForm(forms.Form):

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)


class AddEmailForm(UserForm):

    email = forms.EmailField(label=_("E-mail"),
                             required=True,
                             widget=forms.TextInput(attrs={"type": "email",
                                                           "size": "30"}))

    def clean_email(self):
        value = self.cleaned_data["email"]
        value = get_adapter().clean_email(value)
        errors = {
            "this_account": _("This e-mail address is already associated"
                              " with this account."),
            "different_account": _("This e-mail address is already associated"
                                   " with another account."),
        }
        emails = EmailAddress.objects.filter(email__iexact=value)
        if emails.filter(user=self.user).exists():
            raise forms.ValidationError(errors["this_account"])
        if app_settings.UNIQUE_EMAIL:
            if emails.exclude(user=self.user).exists():
                raise forms.ValidationError(errors["different_account"])
        return value

    def save(self, request):
        return EmailAddress.objects.add_email(request,
                                              self.user,
                                              self.cleaned_data["email"],
                                              confirm=True)


class ChangePasswordForm(UserForm):

    oldpassword = PasswordField(label=_("Current Password"))
    password1 = SetPasswordField(label=_("New Password"))
    password2 = PasswordField(label=_("New Password (again)"))

    def clean_oldpassword(self):
        if not self.user.check_password(self.cleaned_data.get("oldpassword")):
            raise forms.ValidationError(_("Please type your current"
                                          " password."))
        return self.cleaned_data["oldpassword"]

    def clean_password2(self):
        if ("password1" in self.cleaned_data
                and "password2" in self.cleaned_data):
            if (self.cleaned_data["password1"]
                    != self.cleaned_data["password2"]):
                raise forms.ValidationError(_("You must type the same password"
                                              " each time."))
        return self.cleaned_data["password2"]

    def save(self):
        get_adapter().set_password(self.user, self.cleaned_data["password1"])


class SetPasswordForm(UserForm):

    password1 = SetPasswordField(label=_("Password"))
    password2 = PasswordField(label=_("Password (again)"))

    def clean_password2(self):
        if ("password1" in self.cleaned_data
                and "password2" in self.cleaned_data):
            if (self.cleaned_data["password1"]
                    != self.cleaned_data["password2"]):
                raise forms.ValidationError(_("You must type the same password"
                                              " each time."))
        return self.cleaned_data["password2"]

    def save(self):
        get_adapter().set_password(self.user, self.cleaned_data["password1"])


class ResetPasswordForm(forms.Form):

    email = forms.EmailField(
        label=_("E-mail"),
        required=True,
        widget=forms.TextInput(attrs={"type": "email", "size": "30"}))

    def clean_email(self):
        email = self.cleaned_data["email"]
        email = get_adapter().clean_email(email)
        self.users = get_user_model().objects \
            .filter(Q(email__iexact=email)
                    | Q(emailaddress__email__iexact=email)).distinct()
        if not self.users.exists():
            raise forms.ValidationError(_("The e-mail address is not assigned"
                                          " to any user account"))
        return self.cleaned_data["email"]

    def save(self, request, **kwargs):

        email = self.cleaned_data["email"]
        token_generator = kwargs.get("token_generator",
                                     default_token_generator)

        for user in self.users:

            temp_key = token_generator.make_token(user)

            # save it to the password reset model
            # password_reset = PasswordReset(user=user, temp_key=temp_key)
            # password_reset.save()

            current_site = Site.objects.get_current()

            # send the password reset email
            path = reverse("account_reset_password_from_key",
                           kwargs=dict(uidb36=user_pk_to_url_str(user),
                                       key=temp_key))
            url = build_absolute_uri(request, path,
                                     protocol=app_settings.DEFAULT_HTTP_PROTOCOL)
            context = {"site": current_site,
                       "user": user,
                       "password_reset_url": url}
            if app_settings.AUTHENTICATION_METHOD \
                    != AuthenticationMethod.EMAIL:
                context['username'] = user_username(user)
            get_adapter().send_mail('account/email/password_reset_key',
                                    email,
                                    context)
        return self.cleaned_data["email"]


class ResetPasswordKeyForm(forms.Form):

    password1 = SetPasswordField(label=_("New Password"))
    password2 = PasswordField(label=_("New Password (again)"))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.temp_key = kwargs.pop("temp_key", None)
        super(ResetPasswordKeyForm, self).__init__(*args, **kwargs)

    # FIXME: Inspecting other fields -> should be put in def clean(self) ?
    def clean_password2(self):
        if ("password1" in self.cleaned_data
                and "password2" in self.cleaned_data):
            if (self.cleaned_data["password1"]
                    != self.cleaned_data["password2"]):
                raise forms.ValidationError(_("You must type the same"
                                              " password each time."))
        return self.cleaned_data["password2"]

    def save(self):
        get_adapter().set_password(self.user, self.cleaned_data["password1"])