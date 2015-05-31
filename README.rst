
|PypiVersion| |Doc badge| |Travis| |Pypi|

===============
Django-Leonardo
===============

Full featured platform for fast and easy building extensible web applications.

*Don't waste your time searching stable solution for daily problems.*

**Deploy and Enjoy ! No skills required !**

For Users
=========

* CMS, Page, Responsive, Layouts, Themes, Color Variations 
* Widgets, Plugins, 3rd party app integrations
* Frontend Edit, Install modules in one click !
* Eshop, Form Designer, Blog, News, Folio, Links, Navigations, ..
* Media, Folders, Files, Images, Documents, Import - Export, ..
* Authentification, 3rd party backends, SAML standard, ..
* Auto loading modules, LIVE configuration, editable templates, ..

For Developers
==============

* Python, Django, FeinCMS, OpenStack Horizon
* AngularJS, React, Bootstrap, Compress, Bootswatch
* Crispy forms, Floppy forms, Select2
* Filer, DbTemplates, Reversion, Constance
* Haystack, Oscar, Django Admin Bootstrap
* and tons of other apps bundled as modules

Further reading:

* `Demo Site`_ (a reference build of an Leonardo project)
* `Demo Store`_ (a reference build of an Leonardo Store project)
* `Developer Documentation`_
* `User Documentation`_
* `Continuous integration homepage`_

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/django-leonardo/django-leonardo
   :target: https://gitter.im/django-leonardo/django-leonardo?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge

.. image:: https://coveralls.io/repos/django-leonardo/django-leonardo/badge.svg?branch=develop
   :alt: Coverage
   :target: https://coveralls.io/r/django-leonardo/django-leonardo?branch=develop

.. _`Demo Site`: http://demo.cms.robotice.cz
.. _`Demo Store`: http://store.leonardo.robotice.org
.. _`Continuous integration homepage`: http://travis-ci.org/django-leonardo/django-leonardo
.. _`Developer Documentation`: http://django-leonardo.readthedocs.org
.. _`User Documentation`: http://leonardo-documentation.rtfd.org

Core
====

Leonardo in default state has enabled three modules and other can be installed.

* Web - precise FeinCMS integration
* Navigation - common navigation components
* Media - Filer integration with basic widgets
* Search - Haystack integration with Whoosh backend

Extensions
==========

Leonardo provide bundled extensions, which provides pluggable advantages.

Modules
-------

* `Auth`_ - authentication, registration, account management as 3rd party (social) and SAML support to your Leonardo sites
* `Blog`_ - Elephant Blog integration
* `Folio`_ - Portfolio app
* `Forms`_ - Stable Form Designer integration with Remote Forms
* `Eshop`_ - Oscar Ecommerce - FeinCMS integration
* `News`_ - News
* `Links`_ - navigation helpers bundles as Leonardo module
* `Redactor`_ - A lightweight wysiwyg editor for Leonardo
* `Sentry`_ - end-user friendly error page
* `Page Permissions`_ - extend Page and provide new Navigation templates with permissions
* `Analytics`_ -  Analytics service integration for Leonardo projects
* Static - client-side libraries like an AngularJS, React, D3.js, ..


.. _`Auth`: https://github.com/leonardo-modules/leonardo-module-auth
.. _`Forms`: https://github.com/leonardo-modules/leonardo-module-forms
.. _`Blog`: https://github.com/leonardo-modules/leonardo-module-blog
.. _`Folio`: https://github.com/leonardo-modules/leonardo-module-folio
.. _`Eshop`: https://github.com/leonardo-modules/leonardo-module-eshop
.. _`News`: https://github.com/leonardo-modules/leonardo-module-news
.. _`Links`: https://github.com/leonardo-modules/leonardo-module-links
.. _`Redactor`: https://github.com/leonardo-modules/leonardo-module-redactor
.. _`Sentry`: https://github.com/leonardo-modules/leonardo-module-sentry
.. _`Page Permissions`: https://github.com/leonardo-modules/leonardo-module-pagepermissions
.. _`Analytics`: https://github.com/leonardo-modules/leonardo-module-analytics

Themes
------

* `Bootwatch`_
* `AdminLTE`_

.. _`Bootwatch`: https://github.com/leonardo-modules/leonardo-theme-bootswatch
.. _`AdminLTE`: https://github.com/leonardo-modules/leonardo-theme-adminlte

Installation
============

one liner

Wget

.. code-block:: bash

    wget -O - https://github.com/django-leonardo/django-leonardo/raw/develop/contrib/install_leonardo.sh | sh


Install Blog

.. code-block:: bash

    wget -O - https://github.com/django-leonardo/django-leonardo/raw/develop/contrib/install_blog.sh | sh

Install Store

.. code-block:: bash

    wget -O - https://github.com/django-leonardo/django-leonardo/raw/develop/contrib/install_store.sh | sh

CURL

.. code-block:: bash

    curl -L https://github.com/django-leonardo/django-leonardo/raw/develop/contrib/install_leonardo.sh -o install_leonardo.sh
    sh install_leonardo.sh

Python

.. code-block:: bash

    python -c 'import urllib; print urllib.urlopen("https://github.com/django-leonardo/django-leonardo/raw/develop/contrib/install_leonardo.sh").read()' > install_leonardo.sh
    sudo sh install_leonardo.sh

Command by command

.. code-block:: bash

    virtualenv -p /usr/bin/python2.7 leonardo_venv
    cd leonardo_venv
    . $PWD/bin/activate

    pip install django-leonardo

    django-admin startproject --template=https://github.com/django-leonardo/site-template/archive/master.zip myproject

    export PYTHONPATH=$PWD/myproject
    cd ./myproject

    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
    python manage.py sync_all

    echo "from django.contrib.auth.models import User; User.objects.create_superuser('root', 'mail@leonardo.cz', 'admin')" | python manage.py shell

    python manage.py runserver 0.0.0.0:80

Navigate your browser to your_ip/admin and login with ``root:admin``

Bundles
-------

Leonardo defines a group of bundles that can be used
to install Leonardo and the dependencies for a given feature.

You can specify these in your requirements or on the ``pip`` comand-line
by using brackets.  Multiple bundles can be specified by separating them by
commas.

.. code-block:: bash

    $ pip install "django-leonardo[folio]"

    $ pip install "django-leonardo[blog,eshop,static,themes]"

The following bundles are available:

CMS
~~~

* django-leonardo[blog] - ElephantBlog integration

* django-leonardo[folio] - Portfolio with translations

* django-leonardo[forms] - Form Designer and Remote Forms

* django-leonardo[links] - Links

* django-leonardo[pagepermissions] - Page Permissions

Auth
~~~~

* django-leonardo[auth] - All auth

* django-leonardo[saml] - SAML auth backend

Themes
~~~~~~

* django-leonardo[themes] - Leonardo themes [Bootstrap, AdminLTE]

* django-leonardo[adminlte] - AdminLTE theme

Ecommerce
~~~~~~~~~

* django-leonardo[store] -Django-Oscar integration (is not stable !)

Common
~~~~~~

* django-leonardo[sentry] - Raven integration with end-user friendly error page

* django-leonardo[static] - AngularJS, React, BootStrap, D3.js, ..

* django-leonardo[debug] - Debug toolbar

* django-leonardo[tests] - Tools for testing

* django-leonardo[redis] - Redis dep

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
.. |Travis| image:: https://travis-ci.org/django-leonardo/django-leonardo.svg?branch=master
