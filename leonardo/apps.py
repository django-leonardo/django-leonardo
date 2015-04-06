
from django.apps import AppConfig

from django.db.models.signals import pre_save, post_save


class LeonardoConfig(AppConfig):
    name = 'leonardo'
    verbose_name = "Leonardo"

    def ready(self):
        pass
