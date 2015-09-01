
from django.apps import AppConfig

from .widget import *


default_app_config = 'leonardo.module.devel.Config'

LEONARDO_OPTGROUP = ('Devel widgets')


LEONARDO_WIDGETS = [
    ClientInfoWidget,
    VisualTestWidget,
]

LEONARDO_APPS = ['leonardo.module.devel']


class Config(AppConfig):
    name = 'leonardo.module.devel'
    verbose_name = "Development module"
