from django import forms
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import ModelSelect2Widget
from leonardo.forms.fields.dynamic import (DynamicModelChoiceField,
                                           DynamicSelectWidget)
from leonardo.module.media.models import File

FILE_SEARCH_FIELDS = [
    'original_filename__icontains',
    'name__icontains',
    'description__icontains',
    'folder__name__icontains',
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


class FileDynamicSelectWidget(DynamicSelectWidget, FileSelectWidget):
    '''Select2 with add item link'''

    pass


class FileFieldMixin(object):

    def __init__(self, *args, **kwargs):
        super(FileFieldMixin, self).__init__(
            queryset=getattr(self, 'model', File).objects.all(),
            empty_label='---',
            widget=FileDynamicSelectWidget(), *args, **kwargs)


class FileField(FileFieldMixin, DynamicModelChoiceField):
    '''Basic File Field for easy selecting files everywhere'''

    cls_name = 'media.file'
    form_cls = 'leonardo.module.media.admin.file.forms.FileForm'


class FileMultipleField(FileFieldMixin, forms.ModelMultipleChoiceField):
    '''Multiple File Field with select widget'''
    pass
