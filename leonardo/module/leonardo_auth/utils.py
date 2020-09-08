try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime
    now = datetime.now

from django.db import models
from django.utils import six
from django.utils.http import int_to_base36, base36_to_int
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

try:
    from django.contrib.auth import update_session_auth_hash
except ImportError:
    update_session_auth_hash = None


def user_pk_to_url_str(user):
    """
    This should return a string.
    """
    User = get_user_model()
    if (hasattr(models, 'UUIDField') and issubclass(
            type(User._meta.pk), models.UUIDField)):
        if isinstance(user.pk, six.string_types):
            return user.pk
        return user.pk.hex

    ret = user.pk
    if isinstance(ret, six.integer_types):
        ret = int_to_base36(user.pk)
    return str(ret)


def url_str_to_user_pk(s):
    User = get_user_model()
    # TODO: Ugh, isn't there a cleaner way to determine whether or not
    # the PK is a str-like field?
    if getattr(User._meta.pk, 'rel', None):
        pk_field = User._meta.pk.rel.to._meta.pk
    else:
        pk_field = User._meta.pk
    if (hasattr(models, 'UUIDField') and issubclass(
            type(pk_field), models.UUIDField)):
        return s
    try:
        pk_field.to_python('a')
        pk = s
    except ValidationError:
        pk = base36_to_int(s)
    return pk


def logout_on_password_change(request, user):
    # Since it is the default behavior of Django to invalidate all sessions on
    # password change, this function actually has to preserve the session when
    # logout isn't desired.
    if (update_session_auth_hash is not None and
            not app_settings.LOGOUT_ON_PASSWORD_CHANGE):
        update_session_auth_hash(request, user)
