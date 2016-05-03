
from leonardo.utils.settings import dotdict, get_conf_from_module, merge
from leonardo.utils.widgets import (find_widget_class, get_all_widget_classes,
                                    get_grouped_widgets, load_widget_classes,
                                    get_htmltext_widget)

__all__ = ('dotdict', 'get_conf_from_module', 'get_leonardo_modules',
           'merge', 'find_widget_class', 'get_all_widget_classes',
           'get_grouped_widgets',)


def is_leonardo_module(mod):
    """returns True if is leonardo module
    """

    if hasattr(mod, 'default') \
            or hasattr(mod, 'leonardo_module_conf'):
        return True
    for key in dir(mod):
        if 'LEONARDO' in key:
            return True
    return False
