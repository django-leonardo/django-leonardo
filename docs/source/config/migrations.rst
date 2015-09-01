
==========
Migrations
==========

Leonardo itself does not come with any migrations. It does not have to: Its
core models haven't changed for several versions now. This does not mean
migrations aren't supported. You are free to use either Django's builtin
migrations support, or also South if you're stuck with Django versions older
than 1.7.

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

If you have database already created, redirect your migration and create empty migrations

add this to your ``settings.py``

.. code-block:: python

    MIGRATION_MODULES = {
        'web': 'leonardo_site.migrations',
    }

create empty migrations to new path

.. code-block:: bash

    python manage.py makemigrations --empty web

For big apps we recommend separation of migrations per module, like this::

    MIGRATION_MODULES = {
        'web': 'leonardo_site.migrations.web',
    }

If you changed ``LANGUAGES`` Django check new migrations, which changed choices on translation of media models. For these purposes we recommend redirect affected apps::

    MIGRATION_MODULES = {
        'web': 'leonardo_site.migrations.web',
        'media': 'leonardo_site.migrations.media',
    }

.. note::

    Don't forget to create corresponding directories.

You can also redirect migrations from any leonardo module. Just use ``MIGRATIONS_MODULES`` in the module descriptor something like this::

    LEONARDO_MIGRATION_MODULES = {
        'web': 'my_module.migrations.web',
        'media': 'my_module.migrations.media',
    }

With this, leonardo supports changing default location ``leonardo_site`` as project module.