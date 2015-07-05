
import floppyforms as forms
from django.core import urlresolvers
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from horizon import tables
from horizon.tables.formset import FormsetDataTable, FormsetRow
from leonardo.module.web.models import PageDimension


class Slider(forms.RangeInput):
    min = 1
    max = 12
    step = 1


class OffsetSlider(Slider):
    min = 0


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


class PageDimensionAddAction(tables.LinkAction):

    name = "dimension_add"
    verbose_name = _("Override page dimension")
    classes = ("ajax-modal", "btn-edit")
    url = "page_dimension_add"

    def get_link_url(self):
        return urlresolvers.reverse(
            self.url, args=[self.table.page_object.id])

    def allowed(self, request, instance):
        return True


class DeletePageDimension(tables.DeleteAction):

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Page Dimension",
            u"Delete Page Dimension",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Page Dimension",
            u"Deleted Page Dimension",
            count
        )

    def delete(self, request, obj_id):
        from ..models import PageDimension
        PageDimension.objects.get(pk=obj_id).delete()


class PageDimensionTable(tables.DataTable):

    formset_class = PageDimensionFormset

    def get_formset(self):
        if self.page_object:
            queryset = self.page_object.dimensions
        else:
            queryset = PageDimension.objects.none()
        if self._formset is None:
            self._formset = self.formset_class(
                self.request.POST or None,
                initial=self._get_formset_data(),
                prefix=self._meta.name,
                queryset=queryset)
        return self._formset

    def __init__(self, request, data=None, needs_form_wrapper=None, **kwargs):

        #self._meta.row_class = PageFormsetRow
        self.page_object = kwargs.pop('page', None)
        super(PageDimensionTable, self).__init__(
            request, data, needs_form_wrapper, **kwargs)

    page = tables.Column('page')
    size = tables.Column('size', verbose_name=_('Size'))
    col1_width = tables.Column('col1_width', verbose_name=('Column 1 Width'))
    col2_width = tables.Column('col2_width', verbose_name=_('Column 2 Width'))
    col3_width = tables.Column('col3_width', verbose_name=_('Column 3 Width'))

    def get_object_id(self, datum):
        return datum.pk

    def get_object_name(self, datum):
        return str(datum)

    name = 'dimensions'

    class Meta:
        name = 'dimensions'
        table_name = 'Dimensions'
        table_actions = (PageDimensionAddAction,)
        row_actions = (DeletePageDimension,)
