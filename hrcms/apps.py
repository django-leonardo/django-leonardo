
from django.apps import AppConfig

from django.db.models.signals import pre_save, post_save


class HRCMSAppConfig(AppConfig):
    name = 'hrcms'
    verbose_name = "hrcms"

    def ready(self):
        pass
