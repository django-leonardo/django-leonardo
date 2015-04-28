
|PypiVersion| |Doc badge| |Travis| |Pypi|

===============
Django-Leonardo
===============

This is a stable for daily use in development.

A collection of awesome Django libraries, resources and shiny things.
Full featured platform for building everything based on Django, FeinCMS, Horizon, Oscar and tons of another apps.

**Don't waste your time searching stable solution for daily problems.**

.. contents::
   :local:

Further reading:

* `Demo site`_ (a reference build of an Leonardo project)
* `Documentation`_
* `Continuous integration homepage`_

.. _`Demo site`: http://demo.cms.robotice.cz
.. _`Continuous integration homepage`: http://travis-ci.org/django-leonardo/django-leonardo
.. _`Documentation`: http://django-leonardo.readthedocs.org

Core
====

Leonardo contains some modules which provide scaffold for all other stuff.

* Web - precise FeinCMS integration
* Navigation - common navigation components
* Media - Filer integration with basic widgets
* Forms - Stable Form builder integration
* Language - basic translation widgets

Extensions
==========

Also Leonardo provide bundled extensions, which provides pluggable advantages.

Modules
-------

* Blog - Elephant Blog integration
* Eshop - Oscar Ecommerce - FeinCMS integration
* Sentry - end-user friendly error page
* Static - client-side libraries like as AngularJS, React, D3.js, ..

Themes
------

* Bootstrap - Bootwatch themes
* AdminLTE

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

    $ pip install "django-leonardo[static]"

    $ pip install "django-leonardo[blog,eshop,static,themes]"

The following bundles are available:

CMS
~~~

* django-leonardo[blog] - ElephantBlog integration

* django-leonardo[static] - AngularJS, React, BootStrap, D3.js, ..

* django-leonardo[themes] - Leonardo themes [Bootstrap, AdminLTE]

* django-leonardo[adminlte] - AdminLTE theme

Ecommerce
~~~~~~~~~

* django-leonardo[eshop] -Django-Oscar integration (is not stable !)

Common
~~~~~~

* django-leonardo[sentry] - Raven integration with end-user friendly error page

Looking for commercial support?
===============================

If you are interested in having an Leonardo project built for you, or for development of an existing Leonardo site. Please get in touch via mail@majklk.cz.

Read More
=========

* http://docs.openstack.org/developer/horizon/quickstart.html
* http://feincms-django-cms.readthedocs.org/en/latest/index.html
* https://django-oscar.readthedocs.org/en/releases-1.0/

.. |Doc badge| image:: https://readthedocs.org/projects/django-leonardo/badge/?version=develop
.. |Pypi| image:: https://pypip.in/d/django-leonardo/badge.svg?style=flat
.. |PypiVersion| image:: https://pypip.in/version/django-leonardo/badge.svg?style=flat
.. |Travis| image:: https://travis-ci.org/django-leonardo/django-leonardo.svg?branch=develop

