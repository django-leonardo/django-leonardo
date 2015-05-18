
"""
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

"""

from django.contrib.messages import constants
from django.contrib.auth.models import User
from horizon.messages import add_message

try:
    from async_messages import messages
    ASYNC = True
except ImportError:
    ASYNC = False


def _get_user(request):

    if isinstance(request, User):
        return request
    if hasattr(request, 'user'):
        return request.user
    return None


def debug(request, message, extra_tags='', fail_silently=False, async=False):
    """Adds a message with the ``DEBUG`` level."""
    if ASYNC and async:
        messages.debug(_get_user(request), message)
    else:
        add_message(request, constants.DEBUG, message, extra_tags=extra_tags,
                    fail_silently=fail_silently)


def info(request, message, extra_tags='', fail_silently=False, async=False):
    """Adds a message with the ``INFO`` level."""
    if ASYNC and async:
        messages.info(_get_user(request), message)
    else:
        add_message(request, constants.INFO, message, extra_tags=extra_tags,
                    fail_silently=fail_silently)


def success(request, message, extra_tags='', fail_silently=False, async=False):
    """Adds a message with the ``SUCCESS`` level."""
    if ASYNC and async:
        messages.success(_get_user(request), message)
    else:
        add_message(request, constants.SUCCESS, message, extra_tags=extra_tags,
                    fail_silently=fail_silently)


def warning(request, message, extra_tags='', fail_silently=False, async=False):
    """Adds a message with the ``WARNING`` level."""
    if ASYNC and async:
        messages.debug(_get_user(request), message)
    else:
        add_message(request, constants.WARNING, message, extra_tags=extra_tags,
                    fail_silently=fail_silently)


def error(request, message, extra_tags='', fail_silently=False, async=False):
    """Adds a message with the ``ERROR`` level."""
    if ASYNC and async:
        messages.debug(_get_user(request), message)
    else:
        add_message(request, constants.ERROR, message, extra_tags=extra_tags,
                    fail_silently=fail_silently)
