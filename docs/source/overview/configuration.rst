
======================
Leonardo Configuration
======================

Leonardo is Django powered. All important settings is related with standard Django settings, but is there some leonardo specific configuration. 


Apps, modules, themes ..
========================

Leonardo has own specific app/module system. This system is same as Django, but provide some improvements, which makes time for installing and configuring new app shorter

.. code-block:: python

    APPS = ['leonardo']

    # is same as

    INSTALLED_APPS = ['leonardo'] 

But if configured via ``APPS``, Leonardo tryies find ``default`` configuration in main descriptor of module.
Descriptor may contains many various properties, which is safely merge into main settings. For full description see ``modules``.

Frontend Edit
=============

.. code-block:: python

    LEONARDO_FRONTEND_EDITING = True

Media
=====

Configuring filer is described in ``module/media``, but is there some nessesary parts

.. code-block:: python

    FILER_IMAGE_MODEL = 'leonardo.module.media.models.Image'


Horizon
=======

Horizon has own ``urls`` finder, which provide capabilities for defining ``dashboards``, ``panels``.. in default state is included in main leonardo's urls, but you can turn off, but you must map external app to any ``Page`` which provide ``horizon`` namespace.

.. code-block:: python

    HORIZON_ENABLED = False

.. note::

	Before this, please add external app ``Horizon`` to any ``Page``, because may broke admin.