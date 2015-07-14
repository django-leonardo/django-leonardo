
==================
Live configuration
==================

Live configuration is based on django-constance with few improvements.

* basic grouping via ``CONSTANCE_CONFIG_GROUPS`` which makes tabs for django admin
* access to config keys from standard django settings
* really live settings, set every value to django settings and respect the default value from them

.. code-block:: python

    class Default(object):

        optgroup = 'GA'

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


All config keys will be namespaced under GA and available from standard django settings::

    from django.conf import settings

    settings.GOOGLE_ANALYTICS_PROPERTY_ID
    -> xx-xxx-x

.. warning::

    This may not work on some special environments like a sqlite. For stable usage in modules we recommend using via ``constance`` see below.

Backends
========

In default state is used database backend but redis is recommended.

Redis
-----

installing via leonardo extras

.. code-block:: bash

    pip install django-leonardo[redis]

set your configuration

.. code-block:: python

    APPS = ['constance.backends.redisd']

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
    
    from django.conf import settings

    if settings.THE_ANSWER == 42:
        answer_the_question()

of via constance module

.. code-block:: python
    
    from constance import config

    if config.THE_ANSWER == 42:
        answer_the_question()
