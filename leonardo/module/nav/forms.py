from leonardo.module.web.widgets.forms import WidgetUpdateForm
from leonardo.module.web.page.widgets import PageSelectWidget
from leonardo.module.web.page.fields import PageSelectField


class NavigationForm(WidgetUpdateForm):

    root = PageSelectField(widget=PageSelectWidget(), required=False)
