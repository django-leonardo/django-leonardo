
======================
Leonardo Configuration
======================

Leonardo is Django powered. All important settings is related with standard Django settings, but is there some leonardo specific configuration. 

Configure files
===============

* ``local_settings`` in your ``PYTHONPATH`` for all stuff
* or ``your_site``/``local``/``settings.py``

.. note::

    ``leonardo_site`` must be in the ``PYTHONPATH``

.. code-block:: python

    SITE_ID = 1
    SITE_NAME = 'leonardo'
    # or full domain
    SITE_DOMAIN = 'www.leonardo.cz'

    LANGUAGE_CODE = 'en'

    RAVEN_CONFIG = {}

.. note::

    Leonardo finds and includes all modules which has descriptor(leonardo modules).

if you want you can specify your custom APPS::

    APPS = [
        'blog',
        'eshop',
        'leonardo_site',  # our app
    ]


Leonardo  template https://github.com/django-leonardo/site-template

.. code-block:: bash
    
    manage.py makemigrations --noinput
    manage.py migrate --noinput
    manage.py sync_all

Change admin site name
======================

.. code-block:: python

    SITE_HEADER = "Leonardo administration"

    SITE_TITLE = "Leonardo site admin"

Apps, modules, themes ..
========================

Leonardo has own specific app/module system. This system is same as Django, but provide some improvements, which makes time for installing and configuring new app shorter

.. code-block:: python

    APPS = ['leonardo']

    # is same as

    INSTALLED_APPS = ['leonardo'] 

But if configured via ``APPS``, Leonardo tryies find ``default`` configuration in main descriptor of module.
Descriptor may contains many various properties, which is safely merge into main settings. For full description see ``modules``.

Leonardo
========

.. code-block:: python

    LEONARDO_MODULE_AUTO_INCLUDE = True

This option says please do not auto include leonardo modules.

.. code-block:: python

    LEONARDO_MEMOIZED = True

If set False is disabled any content cache.

For disable System Module which provide untested and unsecure features.

.. code-block:: python

    LEONARDO_SYSTEM_MODULE = True

Frontend Edit
=============

.. code-block:: python

    LEONARDO_FRONTEND_EDITING = True

Horizon
=======

Horizon has own ``urls`` finder, which provide capabilities for defining ``dashboards``, ``panels``.. in default state is included in main leonardo's urls, but you can turn off, but you must map external app to any ``Page`` which provide ``horizon`` namespace.

.. code-block:: python

    HORIZON_ENABLED = False

.. note::

    Before this, please add external app ``Horizon`` to any ``Page``, because may broke admin.