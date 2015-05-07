
======
Search
======

Leonardo Search is only Haystack integration, which provide robust solution for this domain.

In default state Leonaro use this configuration

.. code-block:: python

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
            'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
        },
    }

For other backends visit

* Sorl - http://django-haystack.readthedocs.org/en/latest/tutorial.html#solr
* ElasticSearch - http://django-haystack.readthedocs.org/en/latest/tutorial.html#elasticsearch
* Xapian - http://django-haystack.readthedocs.org/en/latest/tutorial.html#xapian

.. warning::

    Don't forget rebuild indexes !

.. code-block:: bash

    python manage.py rebuild_index --noinput

For other commands see doc or help.

Enjoy !