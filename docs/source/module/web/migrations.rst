
Migrations
----------

Leonardo itself does not come with any migrations. It does not have to: Its
core models haven't changed for several versions now. This does not mean
migrations aren't supported. You are free to use either Django's builtin
migrations support, or also South if you're stuck with Django versions older
than 1.6.

Django's builtin migrations
---------------------------

* Create a new folder in your app with an empty ``__init__.py`` inside.
* Add the following configuration to your ``settings.py``::

    MIGRATION_MODULES = {
        'web': 'leonardo_site.migrations',
    }

.. code-block:: bash

    python manage.py makemigrations --noinput

    python manage.py migrate --noinput
