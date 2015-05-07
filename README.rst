
|PypiVersion| |Doc badge| |Travis| |Pypi|

===============
Django-Leonardo
===============

This is a stable for daily use in development.

Full featured platform for building everything based on Django, FeinCMS, Horizon, Oscar and tons of another apps.

**Don't waste your time searching stable solution for daily problems.**

Deploy your Bootstrap site in ten minutes !

.. contents::
   :local:

Further reading:

* `Demo site`_ (a reference build of an Leonardo project)
* `Developer Documentation`_
* `User Documentation`_
* `Continuous integration homepage`_

.. _`Demo site`: http://demo.cms.robotice.cz
.. _`Continuous integration homepage`: http://travis-ci.org/django-leonardo/django-leonardo
.. _`Developer Documentation`: http://django-leonardo.readthedocs.org
.. _`User Documentation`: http://leonardo-documentation.rtfd.org

Core
====

Leonardo in default state has enabled three modules and other can be installed.

* Web - precise FeinCMS integration
* Navigation - common navigation components
* Media - Filer integration with basic widgets

Extensions
==========

Leonardo provide bundled extensions, which provides pluggable advantages.

Modules
-------

* `Forms`_ - Stable Form Designer integration with Remote Forms
* `Blog`_ - Elephant Blog integration
* `Eshop`_ - Oscar Ecommerce - FeinCMS integration
* `Sentry`_ - end-user friendly error page
* Static - client-side libraries like an AngularJS, React, D3.js, ..

.. _`Forms`: https://github.com/leonardo-modules/leonardo-module-forms
.. _`Blog`: https://github.com/leonardo-modules/leonardo-module-blog
.. _`Eshop`: https://github.com/leonardo-modules/leonardo-module-eshop
.. _`Sentry`: https://github.com/leonardo-modules/leonardo-module-sentry

Themes
------

* `Bootwatch`_
* `AdminLTE`_

.. _`Bootwatch`: https://github.com/leonardo-modules/leonardo-theme-bootswatch
.. _`AdminLTE`: https://github.com/leonardo-modules/leonardo-theme-adminlte

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
.. |Pypi| image:: https://img.shields.io/pypi/dm/django-leonardo.svg?style=flat
.. |PypiVersion| image:: https://badge.fury.io/py/django-leonardo.svg?style=flat
.. |Travis| image:: https://travis-ci.org/django-leonardo/django-leonardo.svg?branch=develop

