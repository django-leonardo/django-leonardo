
Themes, Templates and Color variations

Sync Themes
-----------

Sync widget themes

.. code-block:: python

    python manage.py sync_all

replace db from files (new version of core template etc..)

.. code-block:: python

    python manage.py sync_all -f

command by command

Run collectstatic

.. code-block:: python

    python manage.py collectstatic --noinput

After collectstatic create page themes

.. code-block:: python

    python manage.py sync_page_themes

load widget themes
    
.. code-block:: python

    python manage.py sync_widget_themes
