
=========
Messagess
=========

Drop-in replacement for django.contrib.messages which handles Leonardo's
messaging needs (e.g. Celery tasks, AJAX communication, etc.).

for async messages install

.. code-block:: bash

    pip install django-async-messages

from https://github.com/codeinthehole/django-async-messages

.. code-block:: python

    >>> from leonardo import messages
    >>> barry = User.objects.get(username='barry')
    >>> messages.debug(barry, "Barry was here")
    >>> messages.info(barry, "Hi, Barry")
    >>> messages.success(barry, "Barry, your report is ready")
    >>> messages.warning(barry, "Barry, you didn't lock your session")
    >>> messages.error(barry, "You are not Barry")

or standard request

.. code-block:: python

    >>> messages.error(request, "You are not Barry")
