
from django.apps import AppConfig
from oscar import get_core_apps as get_eshop_apps


default_app_config = 'leonardo.module.eshop.EshopConfig'


class Default(object):

    optgroup = ('Eshop')

    @property
    def middlewares(self):
        return [
            'oscar.apps.basket.middleware.BasketMiddleware',
        ]

    @property
    def apps(self):
        return [
            'leonardo.module.eshop',
            'leonardo.module.eshop.api',
            'oscarapi'
        ] + get_eshop_apps()

    @property
    def auth_backends(self):
        return ['oscar.apps.customer.auth_backends.EmailBackend']

    @property
    def ctp(self):
        """return WEB Conent Type Processors
        """
        return [
            'oscar.apps.search.context_processors.search_form',
            'oscar.apps.promotions.context_processors.promotions',
            'oscar.apps.checkout.context_processors.checkout',
            'oscar.apps.customer.notifications.context_processors.notifications',
            'oscar.core.context_processors.metadata',
        ]

    @property
    def plugins(self):
        return [
            ('leonardo.module.eshop.urls', 'Eshop', ),
            ('leonardo.module.eshop.api.urls', 'Eshop API', ),
        ]


class EshopConfig(AppConfig, Default):
    name = 'leonardo.module.eshop'
    verbose_name = "Eshop"

    def ready(self):
        """
        from feincms.module.page.models import Page

        pre_save.connect(page_check_options, sender=Page)
        post_save.connect(test, sender=Page)
        """

default = Default()
