
|PypiVersion| |Doc badge| |Pypi|

===============
Django-Leonardo
===============

This is a stable for daily use in development.

A collection of awesome Django libraries, resources and shiny things.
Full featured framework for building everything based on Django, FeinCMS, Horizon, Oscar and tons of another apps.

Fresh modules
=============

- web
- blog
- forms
- lang
- nav
- eshop

Use Cases
=========

- server-side

	- CMS - FeinCMS
	- E-Commerce - Oscar
	- Dashboards - Horizon(OpenStack)
	- API - Django Rest Framework

Features based on
=================

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

Configure files

* ``local_settings`` in your ``PYTHONPATH`` for all stuff
* or ``settings``/``menu`` .. in ``conf``

Minimal config

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
	    'fulltext'
	]

Read More
=========

* http://docs.openstack.org/developer/horizon/quickstart.html
* http://feincms-django-cms.readthedocs.org/en/latest/index.html
* https://django-oscar.readthedocs.org/en/releases-1.0/

.. |Doc badge| image:: https://readthedocs.org/projects/django-leonardo/badge/?version=stable
.. |Pypi| image:: https://pypip.in/d/django-leonardo/badge.svg?style=flat
.. |PypiVersion| image:: https://pypip.in/version/django-leonardo/badge.svg?style=flat
.. [Documentation] http://django-leonardo.readthedocs.org