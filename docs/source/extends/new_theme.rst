
=========
New Theme
=========

Best example is live code, we have two base themes for you and lives under main github group

* AdminLTE - https://github.com/django-leonardo/leonardo-theme-adminlte
* Bootswatch - https://github.com/django-leonardo/leonardo-theme-bootswatch

As you can see theme must contains one template for page layout and optionaly base css for this layout and some color variations lives in ``skins`` directory.

Directory structure::

    leonardo_theme_bootswatch
        |-- __init__.py
        |-- templates
            |-- base
                |-- page
                    |-- bootswatch.html
        |-- static
            |-- themes
                |-- bootswatch
                    |-- _variables.scss
                    |-- cosmo
                        |-- _variables.scss
                        |-- _styles.scss
                        |-- scheme.scss


Required stuff for color sheme is ``scheme.scss`` which may contains something like this::

    @import "_variables";
    @import "../_styles";
    @import "_styles";

.. warning::

    Every skin must have ``_variables`` file which is dynamically appended to every widget scss file.

If we run

.. code-block:: python

    python manage.py sync_all

or any his variations Leonardo load base page templates into database and after this step tries find css in theme location.
After that we have ready theme for our pages and also for editing via admin interface.

Leonardo automatically load these tested themes if is present. For their installation write this in your environment

For all supported themes simple do

.. code-block:: python

    pip install django-leonardo[themes]

    python manage.py sync_all -f

sync themes

.. code-block:: python

    python manage.py sync_all -f

Solo AdminLTE

.. code-block:: bash

    pip install leonardo_theme_adminlte
    
    # or via main package

    pip install django-leonardo[adminlte]

.. note::

    Don't remmeber sync themes, which is described in the ``web/themes``

For new theme is situation more complex. You have two options:

* create your Leonardo module descriptor and put your theme name into main ``APPS``
* pur your theme name directly into main ``INSTALLED_APPS``, but this is more hard way

For first option you must write simple leonardo module descriptor in ``my_new_theme_name/__init__.py``

.. code-block:: python

    class Default(object):

        # define your specific apps
        apps = ['my_new_theme_name']

    default = Default()

and add it to APPS in ``local_settings.py``

.. code-block:: python

    APPS = [
        'my_new_theme_name'
    ]

That's it. Run ``sync_all``.
