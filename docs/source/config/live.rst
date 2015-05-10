
==================
Live configuration
==================

Live configuration is based on django-constance.

Redis
=====

Leonardo configuration use ``database`` backend in default state, but if you run

.. code-block:: bash

    pip install django-leonardo[redis]

will be installed backend for redis now you must set your configuration

.. code-block:: python

    APPS = ['constance.backends.database']

    CONSTANCE_BACKEND = 'constance.backends.redisd.RedisBackend'

    CONSTANCE_REDIS_CONNECTION = {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
    }

optionaly 

.. code-block:: python

    CONSTANCE_REDIS_PREFIX = 'constance:myproject:'

for more configuration choices visit http://django-constance.readthedocs.org/en/latest/backends.html

Using in your code
==================

.. code-block:: python
    
    from constance import config

    # ...

    if config.THE_ANSWER == 42:
        answer_the_question()

leonardo syncs all defaults to main settings file

.. code-block:: python

    from django.conf import settings

    if settings.THE_ANSWER == 42:
        answer_the_question()

.. warning::

    This may not work on some special environments like a sqlite. For stable usage in modules we recommend using via ``constance``

Using in the Leonardo module
============================

    class Default(object):

        apps = [
            'analytical',
            'leonardo_module_analytics',
        ]

        config = {
            'GOOGLE_ANALYTICS_PROPERTY_ID': ('xx-xxx-x', _('Google Site identificator')),
            'GOOGLE_ANALYTICS_SITE_SPEED': (False, _('analyze page speed')),
            'GOOGLE_ANALYTICS_ANONYMIZE_IP': (False, _('anonymize ip')),
        }

    default = Default()

.. note::

    Please be sure about keys in config, all is merged into one big dictionary which is used. Last wins.
