
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

LEONARDO_WIDGETS = [
    'leonardo.module.leonardo_auth.models.UserLoginWidget',
    'leonardo.module.leonardo_auth.models.UserRegistrationWidget'
]

LEONARDO_APPS = ['leonardo.module.leonardo_auth']

default_app_config = 'leonardo.module.leonardo_auth.Config'

LEONARDO_OPTGROUP = 'Auth widgets'

LEONARDO_PAGE_ACTIONS = ['leonardo_auth/_actions.html']


class Config(AppConfig):
    name = 'leonardo.module.leonardo_auth'
    verbose_name = _("Auth module")
