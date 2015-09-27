from django_select2 import AutoModelSelect2Field, AutoModelSelect2MultipleField

FILE_SEARCH_FIELDS = [
    'original_filename__icontains',
    'name__icontains',
    'description__icontains',
]

FOLDER_SEARCH_FIELDS = [
    'name__icontains',
]


class FileFieldMixin(object):
    search_fields = FILE_SEARCH_FIELDS


class FileField(AutoModelSelect2Field, FileFieldMixin):
    empty_values = [u'']


class FileMultipleField(AutoModelSelect2MultipleField, FileFieldMixin):
    empty_values = [u'']
