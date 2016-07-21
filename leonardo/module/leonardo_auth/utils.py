from datetime import timedelta
try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime
    now = datetime.now

from django.contrib import messages
from django.db import models
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import six
from django.utils.http import urlencode
from django.utils.http import int_to_base36, base36_to_int
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

try:
    from django.contrib.auth import update_session_auth_hash
except ImportError:
    update_session_auth_hash = None

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

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