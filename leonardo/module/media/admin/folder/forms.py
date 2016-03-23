from __future__ import unicode_literals

from crispy_forms.bootstrap import *
from crispy_forms.layout import *
from crispy_forms.layout import HTML, Layout
from django import forms
from django.forms.models import modelformset_factory
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from leonardo.forms import SelfHandlingModelForm
from leonardo.module.media.fields.folder import FolderField
from leonardo.module.media.models import Folder
from leonardo.module.media.utils import handle_uploaded_files


class FolderForm(SelfHandlingModelForm):

    id = forms.IntegerField('id',
                            widget=forms.widgets.HiddenInput, required=False)
    folder = forms.HiddenInput()
    parent = FolderField(required=False)
    file = forms.FileField(
        label=_('File'), required=False)
    files = forms.FileField(
        label=_('Folder'), required=False,
        help_text=_('This field may support uploading whole folder'))

    def handle(self, request, data):
        data = self.clean_data(data)
        return super(FolderForm, self).handle(request, data)

    def handle_related_models(self, request, folder):

        files = []

        if len(request.FILES.getlist('files')) > 0:
            files = request.FILES.getlist('files')
        else:
            files = request.FILES.getlist('file')

        if len(files) > 0:
            handle_uploaded_files(files, folder, request.user)

    def clean_data(self, data):
        data.pop('file')
        data.pop('files')
        return data

    def __init__(self, *args, **kwargs):
        super(FolderForm, self).__init__(*args, **kwargs)

        files_area = ''

        if 'id' in kwargs.get('initial'):

            folder = Folder.objects.get(id=kwargs['initial']['id'])
            files_area = render_to_string(
                'admin/media/folder/directory_table_modal.html',
                {'files': folder.files.all()})

        self.fields['files'].widget.attrs["webkitdirectory"] = ""
        self.fields['files'].widget.attrs["directory"] = ""
        self.fields['files'].widget.attrs["mozdirectory="""] = ""

        self.helper.layout = Layout(
            TabHolder(
                Tab(_('Folder'),
                    'id', 'folder', 'name', 'parent',
                    ),
                Tab(_('Files'),
                    Div(Field('file'),
                        css_class="col-lg-6 field-wrapper"),
                    Div(Field('files'),
                        css_class="col-lg-6 field-wrapper"),
                    HTML('''
                        <a href="#" id="add-another" class="btn fa fa-plus">Add</a>
                        <script>
                        $(function() {
                            $('#add-another').click(function() {
                                var cloned = $("#id_file").clone();
                                cloned.val(null);
                                $(cloned).insertAfter("#id_file");
                             });
                            });
                        </script>
                        '''), HTML(files_area)
                    ),
            )
        )

    class Meta:
        model = Folder
        exclude = tuple()


FolderFormset = modelformset_factory(
    Folder, form=FolderForm, can_delete=True, extra=1)
