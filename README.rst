
===============
Django-Leonardo
===============

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
        |-- config
            |-- __init__.py
            |-- admin.py
            |-- menu.py
            |-- settings.py
        |-- local
            |-- __init__.py
            |-- local_settings.py
        |-- static
            |-- css
            |-- js

Configure parts

* First we load all stuff from ``config`` dir, here can be app settings
* Secondary we load configs from ``local`` which can be easily generated from Configuration Management Tools
* If we found some supported ``APPS`` like a ``blog``, ``cms``, ``eshop`` we configure other required stuff for this cases.
* Or use ``local_settings`` in your ``PYTHONPATH`` for all stuff

Other configs

* conf/feincms.py
* conf/menu.py

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
	    'oauth',
	    'reversion',
	    'fulltext'
	]

This settings start full app with default settings.

Note: If we generate config to ``local`` we recommend add ``local`` directory to ``.gitignore``

Read More
=========
