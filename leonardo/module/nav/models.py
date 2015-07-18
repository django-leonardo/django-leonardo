
from leonardo.module.web.models import Widget
from leonardo.module.nav.mixins import NavigationWidgetMixin


class NavigationWidget(Widget, NavigationWidgetMixin):

    """Base class for navigation widget
    """
    pass

    class Meta:
        abstract = True
