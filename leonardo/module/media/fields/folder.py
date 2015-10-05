
from django_select2 import forms
from django import forms as django_forms
from ..models import Folder
from .utils import FOLDER_SEARCH_FIELDS, FileField, FileMultipleField


class FolderPathSelectWidget(forms.Select2Widget):
    search_fields = FOLDER_SEARCH_FIELDS


class FolderSelectWidget(forms.ModelSelect2Widget):
    model = Folder
    search_fields = FOLDER_SEARCH_FIELDS


class FolderFieldMixin(object):

    def label_from_instance(self, obj):
        """
        Coerces ``value`` to a Python data type.
        """
        return obj.pretty_logical_path

    def __init__(self, *args, **kwargs):
        super(FolderFieldMixin, self).__init__(
            queryset=Folder.objects.all(),
            empty_label="---",
            widget=FolderSelectWidget(), *args, **kwargs)


class FolderField(FolderFieldMixin, django_forms.ModelChoiceField):
    '''Folder field for selecting folders, which has human readable label'''
    pass


class FolderMultipleField(FolderFieldMixin, FileMultipleField):
    '''Multiple Select Folder field.'''

    pass
