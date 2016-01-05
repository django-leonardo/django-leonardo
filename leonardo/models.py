import six
from leonardo.module.web.models import *
from leonardo.module.web.models import Page
from . import settings
from leonardo.module.web.widget import ApplicationWidget
from importlib import import_module


def get_class_from_string(widget):
    mod = '.'.join(widget.split('.')[0:-1])
    cls_name = widget.split('.')[-1]
    return mod, cls_name


def register_widgets():
    """
    Register all collected widgets from settings
    WIDGETS = [('mymodule.models.MyWidget', {'mykwargs': 'mykwarg'})]
    WIDGETS = ['mymodule.models.MyWidget', MyClass]
    """

    # special case
    # register external apps
    Page.create_content_type(
        ApplicationWidget, APPLICATIONS=settings.APPLICATION_CHOICES)

    for _optgroup, _widgets in six.iteritems(settings.WIDGETS):
        optgroup = _optgroup if _optgroup != 'ungrouped' else None
        for widget in _widgets:

            kwargs = {'optgroup': optgroup}

            # load class from strings
            if isinstance(widget, six.string_types):
                try:
                    mod, cls_name = get_class_from_string(widget)
                    WidgetCls = getattr(import_module(mod), cls_name)
                except Exception as e:
                    raise e
            elif isinstance(widget, tuple):
                try:
                    mod, cls_name = get_class_from_string(widget[0])
                    if len(widget) > 1:
                        kwargs.update(widget[1])
                    WidgetCls = getattr(import_module(mod), cls_name)
                except Exception as e:
                    raise Exception('%s: %s' % (mod, e))
            else:
                WidgetCls = widget

            Page.create_content_type(
                WidgetCls, **kwargs)


register_widgets()
Page.register_extensions(*settings.PAGE_EXTENSIONS)
Page.register_default_processors(True)
