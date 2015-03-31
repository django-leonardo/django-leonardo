
=====
dhCMS
=====

A collection of awesome Django libraries, resources and shiny things.
Full featured framework for building everything based on Django, FeinCMS, Horizon, Oscar and tons of another apps.


Uses
====

- Backend

	- Django 1.4 +
	- FeinCMS
	- Horizon
	- Oscar
	- Oscar API
	- Form Designer
	- Remote Forms
	- Django Rest Framework

- Client

	- AngularJS
	- ReactJS
	- Bootstrap 3
	- ...

Installation
============

.. code-block:: bash

	pip install django-hrcms

	manage.py runserver 0.0.0.0:80

Scaffold new app
================

Directory structure::

    my_site
        |-- __init__.py
        |-- local
            |-- __init__.py
            |-- settings.py
            |-- menu.py
            |-- admin.py
        |-- static
            |-- css
            |-- js

APPS = [
    'cms',
    'blog',
    'eshop',
]

Minimal config

.. code-block:: python

	SITE_ID = 1
	SITE_NAME = 'hrcms'
	SITE_DOMAIN = 'www.hrcms.cz'

	LANGUAGE_CODE = 'cs'

	RAVEN_CONFIG = {}

	APPS = [
	    'cms',
	    'blog',
	    'eshop',
	]

All settings will be included from local

Note: we recommend ``local`` in ``.gitignore``

Read More
=========
