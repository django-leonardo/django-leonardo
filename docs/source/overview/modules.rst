
==================
Modules and Themes
==================

This part describes, how Leonardo loads and works with extensions.

Basics
======

Extending Leonardo is easy as possible, has two main stones, which support many various scenarios and also can be combined.

* Theme - Templates, CSS, etc - client-side character
* Module - core features, simple wrapper around of another app or anything else

Theme
-----

So best example is live code, we have two base themes for you and lives under main github group

* AdminLTE - https://github.com/django-leonardo/leonardo-theme-adminlte
* Bootswatch - https://github.com/django-leonardo/leonardo-theme-bootswatch

Leonardo automatically load these tested themes if is present. For their installation write this in your environment

For all supported themes simple do

.. code-block:: python

    pip install django-leonardo[themes]

    python manage.py sync_all -f

sync themes

.. code-block:: python

    python manage.py sync_all -f

Solo AdminLTE

.. code-block:: bash

    pip install leonardo_theme_adminlte
    
    # or via main package

    pip install django-leonardo[adminlte]

.. note::

    Don't remmeber sync themes, which is described in the ``web/themes``

For new theme is situation more complex. You have two options:

* create your Leonardo module descriptor and put your theme name into main ``APPS``
* pur your theme name directly into main ``INSTALLED_APPS``, but this is more hard way

For first option you must write simple leonardo module descriptor in ``my_new_theme_name/__init__.py``

.. code-block:: python

    class Default(object):

        # define your specific apps
        apps = ['my_new_theme_name']

    default = Default()

and add it to APPS in ``local_settings.py``

.. code-block:: python

    APPS = [
        'my_new_theme_name'
    ]

That's it. Run ``sync_all``.


Full example

.. code-block:: python

    from django.apps import AppConfig
    from oscar import get_core_apps as get_eshop_apps
    from django.utils.translation import ugettext_lazy as _


    default_app_config = 'leonardo_module_eshop.EshopConfig'

    class Default(object):

        optgroup = ('Eshop')

        #urls_conf = 'oscar.urls'

        @property
        def middlewares(self):
            return [
                'oscar.apps.basket.middleware.BasketMiddleware',
            ]

        @property
        def apps(self):
            return [
                'leonardo_module_eshop',
                'leonardo_module_eshop.api',
                'oscarapi',
                'whoosh',
                'oscar.apps.customer',
            ] + get_eshop_apps()

        @property
        def auth_backends(self):
            return ['oscar.apps.customer.auth_backends.EmailBackend']

        @property
        def ctp(self):
            """return WEB Conent Type Processors
            """
            return [
                #'oscar.apps.search.context_processors.search_form',
                'oscar.apps.promotions.context_processors.promotions',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
            ]

        @property
        def plugins(self):
            return [
                ('leonardo_module_eshop.apps.eshop', 'Eshop', ),
                ('leonardo_module_eshop.apps.cart', 'Shopping Cart', ),
                ('leonardo_module_eshop.apps.customer', 'Customers', ),
                ('leonardo_module_eshop.apps.catalog', _('Eshop Catalog'), {'namespace': 'catalogue'}),
                ('leonardo_module_eshop.apps.api', 'Eshop API', ),
            ]

        """
        @property
        def dirs(self):
            from oscar import OSCAR_MAIN_TEMPLATE_DIR
            return [OSCAR_MAIN_TEMPLATE_DIR]
        """


    class EshopConfig(AppConfig, Default):
        name = 'leonardo_module_eshop'
        verbose_name = "Eshop"

        def ready(self):
            """
            from feincms.module.page.models import Page

            pre_save.connect(page_check_options, sender=Page)
            post_save.connect(test, sender=Page)
            """

    default = Default()

