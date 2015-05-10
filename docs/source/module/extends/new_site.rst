
========
New Site
========

Easiest way how you can create new Leonardo Site is our Django Site Template which lives here

https://github.com/django-leonardo/site-template

If you have installed Leonardo simply type

.. code-block:: bash

    django-admin startproject --template=https://github.com/django-leonardo/site-template/archive/master.zip myproject

    cd myproject

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
        'blog',
        'leonardo_site',  # our app
    ]

Leonardo  template https://github.com/django-leonardo/site-template

If you have configured your database and other common stuff run

.. code-block:: bash
    
    manage.py makemigrations --noinput
    manage.py migrate --noinput
    manage.py sync_all