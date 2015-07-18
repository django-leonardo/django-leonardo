
from django.apps import AppConfig

from .widget import *

LEONARDO_WIDGETS = [
    UserLoginWidget,
    UserRegistrationWidget
]

LEONARDO_APPS = ['leonardo.module.leonardo_auth']

default_app_config = 'leonardo.module.leonardo_auth.Config'

LEONARDO_OPTGROUP = 'Auth widgets'


class Config(AppConfig):
    name = 'leonardo.module.leonardo_auth'
    verbose_name = "Auth module"
