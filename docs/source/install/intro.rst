
============
Installation
============

Installation Leonardo depend's on your case. See some examples

Via PIP

.. code-block:: bash

    pip install django-leonardo

    # or latest

    pip install git+https://github.com/django-leonardo/django-leonardo@develop#egg=leonardo

one liner

Wget

.. code-block:: bash

    wget -O install_leonardo.sh https://github.com/django-leonardo/django-leonardo/raw/develop/contrib/install_leonardo.sh && sh install_leonardo.sh

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

    pip install django-leonardo==2015.0.4

    django-admin startproject --template=https://github.com/django-leonardo/site-template/archive/master.zip myproject

    export PYTHONPATH=$PWD/myproject
    cd ./myproject

    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
    python manage.py sync_all

    echo "from django.contrib.auth.models import User; User.objects.create_superuser('root', 'mail@leonardo.cz', 'admin')" | python manage.py shell

    python manage.py runserver 0.0.0.0:80

Using salt

With configured Salt use our Formula writte your pillars and run

.. code-block:: bash

    salt-call state.sls leonardo

Bootstrap site
--------------

We don't repeat yourself and for really quick start with new site we provide simple API called Bootstrap which has simple format in ``yaml`` or ``json`` and may have contains basic stuff for your site::

    auth.User:
      admin:
        password: root
        mail: root@admin.cz
    web.Page:
      QuickStart:
        title: Quickstart
        slug: quickstart
        override_url: /
        featured: false
        theme: __first__
        in_navigation: true
        active: true
        color_scheme: __first__
        content:
          header:
            web.SiteHeadingWidget:
              attrs:
                site_title: Leonardo Site
                content_theme: navbar
                base_theme: default
              dimenssions:
                md: 2
            web.TreeNavigationWidget:
              attrs:
                depth: 2
                content_theme: navbar
                base_theme: default
              dimenssions:
                md: 6
            web.UserLoginWidget:
              attrs:
                inline: true
                type: 2
                content_theme: navbar
                base_theme: default
              dimenssions:
                md: 4
    elephantblog.Entry:
      Test:
        title: Test
        slug: test
        author:
          type: auth.User
          pk: 1
        content:
          main:
            elephantblog.HtmlTextWidget:
              attrs:
                text: Hello world !
                content_theme: default
                base_theme: default
              dimenssions:
                md: 2

.. code-block:: bash

    python manage.py bootstrap_site --name=demo.yaml

.. note::

    Examples lives in the ``LEONARDO_BOOTSTRAP_DIR`` which is set to ``leonardo/contrib/bootstrap`` in default state.

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

