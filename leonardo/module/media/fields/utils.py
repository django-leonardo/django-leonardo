from django_select2 import AutoModelSelect2Field, AutoModelSelect2MultipleField

FILE_SEARCH_FIELDS = [
    'original_filename__icontains',
    'name__icontains',
    'description__icontains',
]

FOLDER_SEARCH_FIELDS = [
    'name__icontains',
]


class LabelFieldMixin(object):

    def label_from_instance(self, obj):
        """
        Coerces ``value`` to a Python data type.
        """
        return obj.pretty_logical_path


class FileFieldMixin(LabelFieldMixin):
    search_fields = FILE_SEARCH_FIELDS


class FileField(FileFieldMixin, AutoModelSelect2Field):
    empty_values = [u'']


class FileMultipleField(FileFieldMixin, AutoModelSelect2MultipleField):
    empty_values = [u'']
