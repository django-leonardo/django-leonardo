from django import forms
from django_select2.forms import ModelSelect2Widget
from leonardo.module.media.models import File

FILE_SEARCH_FIELDS = [
    'original_filename__icontains',
    'name__icontains',
    'description__icontains',
]

FOLDER_SEARCH_FIELDS = [
    'name__icontains',
]


class FileSelectWidget(ModelSelect2Widget):

    model = File

    search_fields = FILE_SEARCH_FIELDS

    def label_from_instance(self, obj):
        """
        Coerces ``value`` to a Python data type.
        """
        return obj.pretty_logical_path


class FileFieldMixin(object):
    empty_label = "(Nothing)"

    widget = FileSelectWidget()

    def __init__(self, *args, **kwargs):
        super(FileFieldMixin, self).__init__(
            self.queryset, self.empty_label, *args, **kwargs)


class FileField(FileFieldMixin, forms.ModelChoiceField):

    pass


class FileMultipleField(FileFieldMixin, forms.ModelMultipleChoiceField):
    pass
