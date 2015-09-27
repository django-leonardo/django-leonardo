from leonardo.module.web.fields import PageSelectField
from leonardo.module.web.widgets.forms import WidgetUpdateForm
from leonardo.fields import SimpleSelect2Widget


class NavigationForm(WidgetUpdateForm):

    root = PageSelectField(widget=SimpleSelect2Widget(), required=False)
