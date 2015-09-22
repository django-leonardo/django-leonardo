
import logging
from django.apps import AppConfig

default_app_config = 'leonardo.module.system.Config'

LOG = logging.getLogger(__name__)


class Default(object):

    optgroup = 'System'

    apps = ['leonardo.module.system']

    urls_conf = 'leonardo.module.system.urls'

    page_actions = ['system/module_actions.html']


class Config(AppConfig, Default):
    name = 'leonardo.module.system'
    verbose_name = "Leonardo System Module"

default = Default()
