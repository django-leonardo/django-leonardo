
from django_select2 import forms
from ..models import Folder
from .utils import FOLDER_SEARCH_FIELDS, FileField, FileMultipleField


class FolderPathSelectWidget(forms.Select2Widget):
    search_fields = FOLDER_SEARCH_FIELDS


class FolderSelectWidget(forms.ModelSelect2Widget):
    model = Folder
    search_fields = FOLDER_SEARCH_FIELDS

    def label_from_instance(self, obj):
        """
        Coerces ``value`` to a Python data type.
        """
        return obj.pretty_logical_path


class FolderField(FileField):
    queryset = Folder.objects
    empty_label = "(Nothing)"
    widget = FolderSelectWidget()


class FolderMultipleField(FileMultipleField):
    queryset = Folder.objects
    search_fields = FOLDER_SEARCH_FIELDS
    widget = FolderSelectWidget()
