
==================
Live configuration
==================

Live configuration is based on django-constance with few improvements.

* basic grouping via ``CONSTANCE_CONFIG_GROUPS`` which makes tabs for django admin
* access to config keys from standard django settings
* really live settings, set every value to django settings and respect the default value from them

Live settings now supports these types:

* String
* Number
* Boolean
* Dict

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
            'Media Thumbnails': {
                'SIZES': ({
                    'SMALL': '64x64',
                    'MEDIUM': '265x265',
                }, 'Help Text')
            }
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
