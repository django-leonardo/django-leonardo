
from django.apps import AppConfig

default_app_config = 'leonardo.module.devel.Config'

LEONARDO_OPTGROUP = ('Devel widgets')


LEONARDO_WIDGETS = [
    'leonardo.module.devel.models.ClientInfoWidget',
    'leonardo.module.devel.models.VisualTestWidget',
]

LEONARDO_APPS = ['leonardo.module.devel']


class Config(AppConfig):
    name = 'leonardo.module.devel'
    verbose_name = "Development module"
