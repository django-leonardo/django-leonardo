
from django.utils import six
from django.conf import settings
from leonardo.module.web.models import Widget


def get_all_widget_classes():
    """returns collected Leonardo Widgets

    if not declared in settings is used __subclasses__
    which not supports widget subclassing

    """
    _widgets = getattr(settings,
                       'WIDGETS', Widget.__subclasses__())
    widgets = []
    if isinstance(_widgets, dict):
        for group, widget_cls in six.iteritems(_widgets):
            widgets.extend(widget_cls)
    elif isinstance(_widgets, list):
        widgets = _widgets
    return widgets


def find_widget_class(name):

    for w_cls in get_all_widget_classes():
        if name.lower() in w_cls.__name__.lower():
            return w_cls
    return None
