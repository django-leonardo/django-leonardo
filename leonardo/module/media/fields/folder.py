
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django_select2 import forms
from leonardo.forms.fields.dynamic import (DynamicModelChoiceField,
                                           DynamicSelectWidget)
from ..models import Folder
from .utils import FOLDER_SEARCH_FIELDS, FileMultipleField


class FolderPathSelectWidget(forms.Select2Widget):
    search_fields = FOLDER_SEARCH_FIELDS


class FolderSelectWidget(FolderPathSelectWidget, DynamicSelectWidget):
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


class FolderField(FolderFieldMixin, DynamicModelChoiceField):
    '''Folder field for selecting folders, which has human readable label'''

    help_text = _("Type to search file or upload new one.")
    cls_name = 'media.folder'
    form_cls = 'leonardo.module.media.admin.folder.forms.FolderForm'

    def __init__(self,
                 add_item_link=None,
                 add_item_link_args=None,
                 search_fields=None,
                 *args,
                 **kwargs):
        super(FolderField, self).__init__(*args, **kwargs)

        if search_fields:
            self.widget.search_fields = search_fields


class FolderMultipleField(FolderFieldMixin, FileMultipleField):
    '''Multiple Select Folder field.'''

    pass
