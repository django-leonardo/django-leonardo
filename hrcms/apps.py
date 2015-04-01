
from django.apps import AppConfig

from hrcms.signals import page_check_options, test
from django.db.models.signals import pre_save, post_save


class HRCMSAppConfig(AppConfig):
    name = 'hrcms'
    verbose_name = "hrcms"

    def ready(self):

        from feincms.module.page.models import Page

        pre_save.connect(page_check_options, sender=Page)
        post_save.connect(test, sender=Page)
