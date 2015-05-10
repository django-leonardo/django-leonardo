
from django.apps import AppConfig


default_app_config = 'testapp.TestAppConfig'


class Default(object):

    apps = ['testapp']

    config = {
        'GOOGLE_ANALYTICS_SITE_SPEED': (False, ('analyze page speed')),
    }


class TestAppConfig(AppConfig, Default):
    name = 'testapp'
    verbose_name = ("Test App")

default = Default()
