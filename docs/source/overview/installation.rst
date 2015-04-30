
============
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


Django
------

Leonardo supports Django 1.8, but for this time requires additional steps with data migrations, because not all 3rd party apps support Dj 1.8, and if someone use South is there problem with migration dependecies.

Some basic steps which allows to you experiment with new Django compatibility

* first you need Django 1.7 installation, created database
* run migrate command
* install django 1.8 (pip install -r Django==1.8)

run your Leonardo on Django 1.8

