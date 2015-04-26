
|PypiVersion| |Doc badge| |Pypi|

===============
Django-Leonardo
===============

This is a stable for daily use in development.

A collection of awesome Django libraries, resources and shiny things.
Full featured framework for building everything based on Django, FeinCMS, Horizon, Oscar and tons of another apps.

**Don't waste your time searching stable solution for daily problems.**

.. contents::
   :local:

Use Cases
=========

- server-side

    - CMS - FeinCMS
    - E-Commerce - Oscar
    - Dashboards - Horizon(OpenStack)
    - API - Django Rest Framework

Features
--------

- Backend

    - Django 1.4 +
    - FeinCMS
        - Page, Blog, Navigation, Form Designer, Remote Forms
    - Horizon / horizon-contrib
        - Dashboards, Panels, Modals, Tables, Tabs, Workflows
    - Oscar
        - Model, Processes, API

- Client

    - AngularJS
        - SortTable, Filters, ..
    - React
    - AdminLTE 2 +
    - Bootstrap 3

Installation
============

.. code-block:: bash

    pip install django-leonardo

    # or latest

    pip install git+https://github.com/django-leonardo/django-leonardo@develop#egg=leonardo

    # start

    manage.py runserver 0.0.0.0:80

Bundles
-------

Leonardo defines a group of bundles that can be used
to install Leonardo and the dependencies for a given feature.

You can specify these in your requirements or on the ``pip`` comand-line
by using brackets.  Multiple bundles can be specified by separating them by
commas.

.. code-block:: bash

    $ pip install "django-leonardo[web]"

    $ pip install "django-leonardo[web,nav,media,eshop]"

The following bundles are available:

CMS
~~~

* django-leonardo[web] - for FeinCMS integration, is one of main parts

* django-leonardo[media] - for using the Filer and related widgets like a Media Gallery, ..

* django-leonardo[nav] - set of navigation widgets

* django-leonardo[blog] - ElephantBlog integration

* django-leonardo[forms] - Form-Builder(FeinCMS) integration with Remote-Forms for API

Ecommerce
~~~~~~~~~

* django-leonardo[eshop] -Django-Oscar integration (is not stable !)


Setup
=====

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

Configuration
-------------

Configure files

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
        'page': 'leonardo.module.web.page',
    }

Override location for our migrations

.. code-block:: python

    MIGRATION_MODULES = {
        'web': 'leonardo_site.migrations',
    }

.. code-block:: bash

    python manage.py makemigrations --noinput

    python manage.py migrate --noinput


Sync Themes
-----------

Sync widget themes

.. code-block:: python

    python manage.py sync_themes

replace db from files (new version of core template etc..)

.. code-block:: python

    python manage.py sync_themes --force

Change admin site name

.. code-block:: python

    SITE_HEADER = "Leonardo administration"

    SITE_TITLE = "Leonardo site admin"

Looking for commercial support?
===============================

If you are interested in having an Leonardo project built for you, or for development of an existing Leonardo site. Please get in touch via mail@majklk.cz.

Read More
=========

* http://docs.openstack.org/developer/horizon/quickstart.html
* http://feincms-django-cms.readthedocs.org/en/latest/index.html
* https://django-oscar.readthedocs.org/en/releases-1.0/

.. |Doc badge| image:: https://readthedocs.org/projects/django-leonardo/badge/?version=stable
.. |Pypi| image:: https://pypip.in/d/django-leonardo/badge.svg?style=flat
.. |PypiVersion| image:: https://pypip.in/version/django-leonardo/badge.svg?style=flat
.. [Documentation] http://django-leonardo.readthedocs.org