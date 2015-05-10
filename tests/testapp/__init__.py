
from django.apps import AppConfig


default_app_config = 'testapp.TestAppConfig'


class Default(object):

    apps = ['testapp']


class TestAppConfig(AppConfig, Default):
    name = 'testapp'
    verbose_name = ("Test App")

default = Default()
