
import floppyforms as forms
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext_lazy as _
from horizon import tables
from horizon.tables.formset import FormsetDataTable, FormsetRow
from leonardo.module.web.models import WidgetDimension, PageDimension


class Slider(forms.RangeInput):
    min = 0
    max = 12
    step = 1


class WidgetDimensionForm(forms.ModelForm):

    width = forms.CharField(widget=Slider(), initial=12)
    height = forms.CharField(widget=Slider(), initial=0)
    offset = forms.CharField(widget=Slider(), initial=0)

    class Meta:
        model = WidgetDimension
        exclude = tuple()

WidgetDimensionFormset = modelformset_factory(
    WidgetDimension, form=WidgetDimensionForm, can_delete=True, extra=1)


class CustomFormsetRow(FormsetRow):

    def __init__(self, column, datum, form):
        self.form = form
        super(CustomFormsetRow, self).__init__(column, datum, form)
        # add initial
        if not datum and column.data:
            try:
                previous = column.data[0]
                self.form.fields['widget_type'].initial = previous.widget_type
                self.form.fields['widget_id'].initial = previous.widget_id
            except Exception:
                pass


class WidgetDimensionTable(FormsetDataTable):

    formset_class = WidgetDimensionFormset

    def get_formset(self):
        """Provide the formset corresponding to this DataTable.

        Use this to validate the formset and to get the submitted data back.
        """
        if self.widget:
            queryset = self.widget.dimensions
        else:
            queryset = WidgetDimension.objects.none()
        if self._formset is None:
            self._formset = self.formset_class(
                self.request.POST or None,
                initial=self._get_formset_data(),
                prefix=self._meta.name,
                queryset=queryset)
        return self._formset

    def __init__(self, *args, **kwargs):
        self._meta.row_class = CustomFormsetRow
        self.widget = kwargs.pop('widget', None)
        super(WidgetDimensionTable, self).__init__(*args, **kwargs)

    widget_id = tables.Column('widget_id', hidden=True)
    widget_type = tables.Column('widget_type', hidden=True)
    size = tables.Column('size', verbose_name=_('Size'))
    width = tables.Column('width', verbose_name=('Width'))
    height = tables.Column('height', verbose_name=_('Height'))
    offset = tables.Column('offset', verbose_name=_('Offset'))

    name = 'dimensions'

    class Meta:
        name = 'dimensions'
        table_name = 'Dimensions'


class PageDimensionForm(forms.ModelForm):

    col1_width = forms.CharField(widget=Slider(), initial=4)
    col2_width = forms.CharField(widget=Slider(), initial=4)
    col3_width = forms.CharField(widget=Slider(), initial=4)

    class Meta:
        model = PageDimension
        exclude = tuple()

PageDimensionFormset = modelformset_factory(
    PageDimension, form=PageDimensionForm, can_delete=True, extra=1)


class PageFormsetRow(FormsetRow):

    def __init__(self, column, datum, form):
        self.form = form
        super(PageFormsetRow, self).__init__(column, datum, form)
        # add initial
        if not datum:
            self.form.fields['page'].initial = self.page_object


class PageDimensionTable(FormsetDataTable):

    formset_class = PageDimensionFormset

    def get_formset(self):
        if self.page_object:
            queryset = self.page_object.own_dimensions
        else:
            queryset = PageDimension.objects.none()
        if self._formset is None:
            self._formset = self.formset_class(
                self.request.POST or None,
                initial=self._get_formset_data(),
                prefix=self._meta.name,
                queryset=queryset)
        return self._formset

    def __init__(self, *args, **kwargs):
        self._meta.row_class = PageFormsetRow
        self.page_object = kwargs.pop('page', None)
        super(PageDimensionTable, self).__init__(*args, **kwargs)

    page = tables.Column('page')
    size = tables.Column('size', verbose_name=_('Size'))
    col1_width = tables.Column('col1_width', verbose_name=('Column 1 Width'))
    col2_width = tables.Column('col2_width', verbose_name=_('Column 2 Width'))
    col3_width = tables.Column('col3_width', verbose_name=_('Column 3 Width'))

    name = 'dimensions'

    class Meta:
        name = 'dimensions'
        table_name = 'Dimensions'
