
from django.apps import AppConfig

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
    verbose_name = "Auth module"
