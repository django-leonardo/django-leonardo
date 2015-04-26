
=============
Configuration
=============

Minimal app
-----------

Directory structure::

    leonardo_site
        |-- __init__.py
        |-- local
            |-- __init__.py
            |-- local_settings.py
        |-- static
            |-- css
            |-- js

Configure files
---------------

* ``local_settings`` in your ``PYTHONPATH`` for all stuff
* or ``settings``/``menu`` .. in ``conf``

.. note::

    ``leonardo_site`` must be in the ``PYTHONPATH``

.. code-block:: python

    SITE_ID = 1
    SITE_NAME = 'leonardo'
    # or full domain
    SITE_DOMAIN = 'www.leonardo.cz'

    LANGUAGE_CODE = 'en'

    RAVEN_CONFIG = {}

    APPS = [
        'web',
        'blog',
        'eshop',
        'fulltext',
        'leonardo_site',  # our app
    ]

Change admin site name
----------------------

.. code-block:: python

    SITE_HEADER = "Leonardo administration"

    SITE_TITLE = "Leonardo site admin"
