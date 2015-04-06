
|PypiVersion| |Doc badge| |Pypi|

===============
Django-Leonardo
===============

A collection of awesome Django libraries, resources and shiny things.
Full featured framework for building everything based on Django, FeinCMS, Horizon, Oscar and tons of another apps.


Features based on
=================

- Backend

	- Django 1.4 +
	- FeinCMS
	- Horizon
	- Horizon Contrib
	- Oscar - ecommerce
	- Oscar API
	- Form Designer
	- Remote Forms
	- Django Rest Framework

- Client

	- AngularJS
	- React
	- Bootstrap 3
	- ...

Installation
============

.. code-block:: bash

	pip install django-leonardo

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