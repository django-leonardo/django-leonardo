
============
Installation
============

Installation Leonardo depend's on your case. See some examples

Via PIP

.. code-block:: bash

    pip install django-leonardo

    # or latest

    pip install git+https://github.com/django-leonardo/django-leonardo@develop#egg=leonardo

WGET one-liner

.. code-block:: bash

    wget -O install_leonardo.sh https://github.com/django-leonardo/django-leonardo/raw/develop/contrib/scripts/install_leonardo.sh && sh install_leonardo.sh

Command by command

.. code-block:: bash

    virtualenv -p /usr/bin/python2.7 leonardo_venv
    cd leonardo_venv
    . $PWD/bin/activate

    pip install -e git+https://github.com/django-leonardo/django-leonardo@develop#egg=django-leonardo
    pip install -r $PWD/src/django-leonardo/requirements.txt
    django-admin startproject --template=https://github.com/django-leonardo/site-template/archive/master.zip myproject

    export PYTHONPATH=$PWD/myproject
    cd myproject

    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
    python manage.py bootstrap_site --url=http://raw.githubusercontent.com/django-leonardo/django-leonardo/develop/contrib/bootstrap/demo.yaml

    echo "from django.contrib.auth.models import User; User.objects.create_superuser('root', 'mail@leonardo.cz', 'admin')" | python manage.py shell

    python manage.py runserver 0.0.0.0:80


Using salt

With configured Salt use our Formula writte your pillars and run

.. code-block:: bash

    salt-call state.sls leonardo

Bundles
-------

Leonardo defines a group of bundles that can be used
to install Leonardo and the dependencies for a given feature.

You can specify these in your requirements or on the ``pip`` comand-line
by using brackets.  Multiple bundles can be specified by separating them by
commas.

For all Leonardo modules continue to https://github.com/leonardo-modules

.. code-block:: bash

    $ pip install "django-leonardo[web]"

    $ pip install "django-leonardo[web,nav,media,eshop]"

The following bundles are available:

CMS
~~~

* django-leonardo[blog] - ElephantBlog integration

* django-leonardo[folio] - Portfolio with translations

* django-leonardo[multisite] - Leonardo multi sites

* django-leonardo[forms] - Form Designer and Remote Forms

* django-leonardo[links] - Links

* django-leonardo[pagepermissions] - Page Permissions

Background Jobs
~~~~~~~~~~~~~~~

* django-leonardo[celery] - Celery Workers for background Jobs

Admin
~~~~~

* django-leonardo[admin] - Django Admin for Leonardo CMS

Auth
~~~~

* django-leonardo[auth] - All auth

* django-leonardo[saml] - SAML auth backend

WYSIWYG Editors
~~~~~~~~~~~~~~~

* django-leonardo[redactor] - Redactor

* django-leonardo[summernote] - SummerNote

Themes
~~~~~~

* django-leonardo[themes] - Leonardo themes [Bootstrap, AdminLTE]

* django-leonardo[adminlte] - AdminLTE theme

Ecommerce
~~~~~~~~~

* django-leonardo[store] - Django-Oscar integration

* django-leonardo[stores] - Django-Oscar Stores

* django-leonardo[cod] - Django-Oscar Cash On Delivery Payment Method

Common
~~~~~~

* django-leonardo[sentry] - Raven integration with end-user friendly error page

* django-leonardo[static] - AngularJS, React, BootStrap, D3.js, ..

* django-leonardo[debug] - Debug toolbar

* django-leonardo[tests] - Tools for testing

* django-leonardo[redis] - Redis dep
