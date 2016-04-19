
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext as _
from leonardo.forms import SelfHandlingModelForm
from leonardo.forms.fields.common import UserField
from leonardo.module.media.fields.folder import FolderField
from leonardo.module.media.models import File


class FileForm(SelfHandlingModelForm):

    folder = FolderField(required=False)
    owner = UserField(required=False)

    def __init__(self, *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)

        if 'sha1' in self.fields:
            self.fields['sha1'].widget.attrs['readonly'] = True

        if '_file_size' in self.fields:
            self.fields['_file_size'].widget.attrs['readonly'] = True

        self.init_layout()

    tabs = {
        'File': {
            'name': _('File'),
            'fields': (
                'id',
                'name',
                'original_filename',
                'file',
                'folder',
                'owner'
            )
        },
        'Advanced': {
            'name': _('Advanced'),
            'fields': (
                'is_public', 'sha1', '_file_size'
            )
        }
    }

    class Meta:
        model = File
        exclude = ()

FileFormset = modelformset_factory(
    File, form=FileForm, can_delete=True, extra=1)
