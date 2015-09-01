
=============================
Leonardo Descriptor Reference
=============================

Descriptor is Leonardo specific and is inspired from Openstack Horizon where is used for non invasive extend Dashboard extends. In the Leonardo we use same pattern, but with some additions.

Directory structure::

    my_awesome_module
        |-- __init__.py
        |-- settings.py
        |-- urls.py

.. warning::

    Leonardo include all settings and urls in root of module.

Descriptor reference
====================

Leonardo
--------

    **apps** - leonardo modules or whatever::

        apps = [
            'leonardo_module_blog',
            'elephantblog',
            'leonardo_module_analytics',
        ]

    **urls_conf** url path to include

    **public** if is set to ``True`` Leonardo does not decorate included url patters for required authentification

    **module_actions** array of templates included in the frontend side bar

FeinCMS
-------

    **widgets** - FeinCMS widgets::

        widgets = [
                BlogCategoriesWidget,
                RecentBlogPostsWidget,
            ]

    **optgroup** - menu group name for widgets::

        optgroup = 'Blog'

    **plugins** - FeinCMS 3rd party apps support::

        plugins = [
            ('elephantblog.urls', 'Blog entries'),
        ]

    **page_extensions** - FeinCMS page extensions

    **navigation_extensions** - FeinCMS Page Extensions - will be imported before reofistering for proper load::

        navigation_extensions = [
            'elephantblog.navigation_extensions.treeinfo',
        ]

Horizon
-------

    **js_files** - merged and added to main page header::

        js_files = [
            'js/redactor.js'
        ]

    **css_files** linked in head as style::

        css_files = [
            'css/redactor.css'
        ]

    **scss_files** linked in head as scss style::

        scss_files = [
            'scss/redactor.scss'
        ]

    **angular_modules** Angular modules which will be loaded::

        angular_modules = [
            'angular-carousel'
        ]

    **js_spec_files** - Angular specific see https://github.com/openstack/horizon/blob/master/openstack_dashboard/enabled/_10_project.py#L44

Constance
---------

    **config** - dictionary of keys for ``django-constance``::

        config = {
            'BLOG_PAGINATE_BY': (10, _('Blog Entries Pagination')),
            'DISQUS_COMMENTS': (False, _('Enable Disqus comments')),
            'DISQUS_SHORTNAME': ('michaelkuty', _('Disqus shortname identificator.')),

        }

Django
------

    **auth_backends** - AUTHENTICATION_BACKENDS::

        auth_backends = [
            'oscar.apps.customer.auth_backends.EmailBackend'
        ]

    **context_processors** - Django Context Processors::

        context_processors = [
            ...
            'oscar.apps.checkout.context_processors.checkout',
            'oscar.apps.customer.notifications.context_processors.notifications',
            ...
        ]

    **middlewares** - Django Middlewares::

        middlewares = [
            'oscar.apps.basket.middleware.BasketMiddleware',
        ]

    **migration_modules** - allow override migration's location::

        migration_modules = {
            'elephantblog': 'leonardo_module_blog.migrations',
        }

    **absolute_url_overrides** - model name and method wich would be imported for easy integrating 3rd party app::

        absolute_url_overrides = {
            'elephantblog.entry': 'leonardo_store.overrides.elephantblog_entry_url_app',
        }


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

        config = {
            'BLOG_PAGINATE_BY': (10, _('Blog Entries Pagination')),
            'DISQUS_COMMENTS': (False, _('Enable Disqus comments')),
            'DISQUS_SHORTNAME': ('michaelkuty', _('Disqus shortname identificator.')),

        }

        navigation_extensions = [
            'elephantblog.navigation_extensions.treeinfo',
        ]

        absolute_url_overrides = {
            'elephantblog.entry': 'leonardo_store.overrides.elephantblog_entry_url_app',
            'elephantblog.categorytranslation':
            'leonardo_store.overrides.elephantblog_categorytranslation_url_app',
        }


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