
=============================
Leonardo Descriptor Reference
=============================

Descriptor is Leonardo specific and is inspired from Openstack Horizon where is used for non invasive extend Dashboard extends. In the Leonardo we use same pattern, but with some additions.

Minimal example
===============

your app directory structure::

    leonardo_module_blog
        |-- __init__.py
        |-- settings.py

__init__.py
-----------

As Django documentations says, you can define your apps in ``apps.py`` or anywhere, in Leonardo we use __init__.py for simplicity. But you can define it where you want.

.. code-block:: python

    from django.apps import AppConfig

    default_app_config = 'leonardo_module_blog.BlogConfig'

    class Default(object):

        optgroup = 'Blog'

        apps = [
            'leonardo_module_blog',
            'elephantblog',
            'leonardo_module_analytics',
        ]

        js_files = [
            'js/redactor.js'
        ]

        css_files = [
            'css/redactor.css'
        ]

    # standard django Application
    class BlogConfig(AppConfig, Default):
        name = 'leonardo_module_blog'
        verbose_name = ("Blog")

    default = Default()  # inicialize

That's all.. Leonardo go throught every module defined in your ``APPS`` and merge all items to main settings file. Complete reference you can see below.


settings.py
-----------

in the settings you may have something like this

.. code-block:: python

    BLOG_TITLE = 'name'

    # whatever

As you expext every key from settings will be inported and merged into main settings file.

.. warning::

	Be careful if you declare keys in the ``module/settings.py``. Every key is imported without special merging process which may override your global settings ! It was designed only for module/app specific defaults.

Descriptor reference
====================

Django
------

    **auth_backends** - AUTHENTICATION_BACKENDS

    **context_processors** - Django Context Processors

    **middlewares** - Django Middlewares

    **migration_modules** - allow override migration's location::

        migration_modules = {
            'elephantblog': 'leonardo_module_blog.migrations',
        }


FeinCMS
-------

    **apps** - leonardo modules or whatever

    **widgets** - FeinCMS widgets

    **optgroup** - menu group name for widgets

    **plugins** - FeinCMS 3rd party apps support   
    
    **page_extensions** - FeinCMS page extensions

Horizon
-------

    **js_files** - merged and added to main page header 

    **css_files** linked in head as style

    **js_spec_files** - Angular specific see https://github.com/openstack/horizon/blob/master/openstack_dashboard/enabled/_10_project.py#L44

Constance
---------

    **config** - dictionary of keys for ``django-constance``