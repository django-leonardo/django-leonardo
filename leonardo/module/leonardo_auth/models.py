
from .widget.userlogin.models import UserLoginWidget
from .widget.registration.models import UserRegistrationWidget
from django.db import models


class GlobalPermission(models.Model):

    """This object is used to global permissions
    """

    class Meta:

        # No database table creation or deletion operations \
        # will be performed for this model.
        managed = False
