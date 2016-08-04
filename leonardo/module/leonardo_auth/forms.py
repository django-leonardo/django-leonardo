from __future__ import absolute_import

from crispy_forms.layout import HTML, Layout
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import \
    default_token_generator as token_generator
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from horizon import forms, messages
from horizon.utils import validators
from horizon_contrib.forms import SelfHandlingForm
from leonardo.utils.emails import send_templated_email as send_mail
from django.conf import settings

from .utils import url_str_to_user_pk, user_pk_to_url_str


class LoginForm(SelfHandlingForm):

    username = forms.CharField(label=_("Username"),
                               max_length=255,
                               widget=forms.TextInput(
                                   attrs={'placeholder':
                                          _('Username'),
                                          'autofocus': 'autofocus'}))

    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(render_value=True))
    remember = forms.BooleanField(label=_("Remember Me"),
                                  required=False)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            "username", "password", "remember",

            HTML('<div class="login-actions"><a href="{}">Sign Up</a><a href="{}">Reset Password</a></div>'.format(reverse("signup"), reverse("reset_pwd")))

        )

    def handle(self, request, data):

        user = authenticate(**data)
        if user is not None:
            if user.is_active:
                login(request, user)

                messages.success(request, "Login success.")
                return True
        messages.error(request, "Login failed.")
        return False


class SignupForm(SelfHandlingForm):

    username = forms.CharField(label=_("Username"),
                               max_length=255,
                               widget=forms.TextInput(
                                   attrs={'placeholder':
                                          _('Username'),
                                          'autofocus': 'autofocus'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'type': 'email',
               'placeholder': _('E-mail address')}))

    password = forms.RegexField(
        label=_("Password"),
        widget=forms.PasswordInput(render_value=False),
        regex=validators.password_validator(),
        error_messages={'invalid': validators.password_validator_msg()})
    confirm_password = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(render_value=False))
    no_autocomplete = True

    def clean(self):
        '''Check to make sure password fields match.'''
        data = super(SignupForm, self).clean()

        # basic check for now
        if 'username' in data:
            if User.objects.filter(
                    username=data['username'],
                    email=data['email']).exists():
                raise validators.ValidationError(
                    _('Username or email exists in database.'))

        if 'password' in data:
            if data['password'] != data.get('confirm_password', None):
                raise validators.ValidationError(_('Passwords do not match.'))
            else:
                data.pop('confirm_password')
        return data

    def handle(self, request, data):

        try:
            user = User.objects.create_user(**data)
            messages.success(
                request,
                _("User account {} was successfuly created.".format(user)))

        except Exception as e:
            raise e
        else:
            data.pop('email')
            return LoginForm().handle(request, data)

        messages.error(request, _("Create Account failed."))
        return False


class UserForm(SelfHandlingForm):

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)


class ChangePasswordForm(UserForm):
    oldpassword = forms.CharField(label=_("Current Password"),
                                  widget=forms.PasswordInput(
        render_value=False))
    password1 = forms.CharField(label=_("New Password"),
                                widget=forms.PasswordInput(
                                    render_value=False))
    password2 = forms.CharField(label=_("New Password (again)"),
                                widget=forms.PasswordInput(
                                    render_value=False))

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

    def handle(self, request, data):
        self.user.set_password(data["password1"])
        self.user.save()

        user = authenticate(
            username=self.user.username,
            password=data["password1"])

        if user is not None:
            if user.is_active:
                login(request, user)

                messages.success(request, "Password changed successfully")
                return True


class ResetPasswordForm(SelfHandlingForm):
    email = forms.EmailField(
        label=_("E-mail"),
        required=True,
        widget=forms.TextInput(attrs={"type": "email", "size": "30"}))

    def clean_email(self):
        email = self.cleaned_data["email"]

        self.users = get_user_model().objects \
            .filter(Q(email__iexact=email)).distinct()

        if not self.users.exists():
            raise forms.ValidationError(_("The e-mail address is not assigned"
                                          " to any user account"))
        return self.cleaned_data["email"]

    def handle(self, request, data):
        email = self.cleaned_data["email"]
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
            url = request.build_absolute_uri(path)

            context = {"site": current_site,
                       "user": user,
                       "password_reset_url": url}
            context['username'] = user.username

            send_mail(
                'Reset password',
                'leonardo_auth/email/password_reset_key.html',
                context,
                [email], settings.DEFAULT_FROM_EMAIL)

        return self.cleaned_data["email"]


class ResetPasswordKeyForm(SelfHandlingForm):

    password1 = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput(render_value=False))

    password2 = forms.CharField(
        label=_("New Password (again)"),
        widget=forms.PasswordInput(render_value=False))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.temp_key = kwargs.pop("temp_key", None)
        super(ResetPasswordKeyForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        if ("password1" in self.cleaned_data
                and "password2" in self.cleaned_data):
            if (self.cleaned_data["password1"]
                    != self.cleaned_data["password2"]):
                raise forms.ValidationError(_("You must type the same"
                                              " password each time."))
        return self.cleaned_data["password2"]

    def handle(self, request, data):
        self.user.set_password(data["password1"])
        self.user.save()
        return True


class UserTokenForm(forms.Form):

    uidb36 = forms.CharField()
    key = forms.CharField()

    reset_user = None

    error_messages = {
        'token_invalid': _('The password reset token was invalid.'),
    }

    def _get_user(self, uidb36):
        User = get_user_model()
        try:
            pk = url_str_to_user_pk(uidb36)
            return User.objects.get(pk=pk)
        except (ValueError, User.DoesNotExist):
            return None

    def clean(self):
        cleaned_data = super(UserTokenForm, self).clean()

        uidb36 = cleaned_data['uidb36']
        key = cleaned_data['key']

        self.reset_user = self._get_user(uidb36)

        if (self.reset_user is None or
                not token_generator.check_token(self.reset_user, key)):
            raise forms.ValidationError(self.error_messages['token_invalid'])

        return cleaned_data
