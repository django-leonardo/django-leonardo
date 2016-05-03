
from django.utils.translation import ugettext_lazy as _
from horizon import tables
from horizon.tables.formset import FormsetDataTable, FormsetRow
from leonardo.module.media.models import File

from .forms import FileFormset


class CustomFormsetRow(FormsetRow):

    def __init__(self, column, datum, category):
        self.category = category
        super(CustomFormsetRow, self).__init__(column, datum, category)
        # add initial
        if not datum and column.data:
            try:
                previous = column.data[0]
                self.category.fields['id'].initial = previous.id + 1
            except Exception:
                pass


class FilesTable(FormsetDataTable):

    formset_class = FileFormset

    def get_formset(self):
        """Provide the formset corresponding to this DataTable.

        Use this to validate the formset and to get the submitted data back.
        """
        if self.folder:
            queryset = self.folder.files.all()
        else:
            queryset = File.objects.none()
        if self._formset is None:
            self._formset = self.formset_class(
                self.request.POST or None,
                initial=self._get_formset_data(),
                prefix=self._meta.name,
                queryset=queryset)
        return self._formset

    def __init__(self, *args, **kwargs):
        self._meta.row_class = CustomFormsetRow
        self.folder = kwargs.pop('folder', None)
        super(FilesTable, self).__init__(*args, **kwargs)

    id = tables.Column('id', hidden=True)
    directory = tables.Column('directory', hidden=True)
    name = tables.Column('name', verbose_name=_("Name"))
    file = tables.Column('file', verbose_name=_("File"))

    name = 'files'

    class Meta:
        name = 'files'
        table_name = 'Files'
