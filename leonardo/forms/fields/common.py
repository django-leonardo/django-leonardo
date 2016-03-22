from django_select2.forms import ModelSelect2Widget
from leonardo.forms.fields.dynamic import (DynamicModelChoiceField,
                                           DynamicSelectWidget)
from django.contrib.auth.models import User


USER_SEARCH_FIELDS = [
    'firs_tname__icontains',
    'last_name__icontains',
    'username__icontains',
    'email__icontains',
]


class UserSelectWidget(ModelSelect2Widget):

    model = User

    search_fields = USER_SEARCH_FIELDS


class UserDynamicSelectWidget(DynamicSelectWidget, UserSelectWidget):
    '''Select2 with add item link'''

    pass


class FieldMixin(object):

    def __init__(self, *args, **kwargs):
        super(FieldMixin, self).__init__(
            queryset=getattr(self, 'model', User).objects.all(),
            empty_label='---',
            widget=UserDynamicSelectWidget(), *args, **kwargs)


class UserField(FieldMixin, DynamicModelChoiceField):
    '''Basic File Field for easy selecting files everywhere'''

    cls_name = 'auth.user'
