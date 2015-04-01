# -#- coding: utf-8 -#-

from .const import *


def build_options(page):
    if hasattr(page, 'parent'):
        try:
            template = page.parent.options['template']
            theme = page.parent.options['theme']
        except:
            template = 'local'
            theme = 'default'
    else:
        template = 'local'
        theme = 'default'

    # TODO load and set layout

    #layout = TEMPLATE_LAYOUTS[page.template_key]

    options = {
        #'col1_width': layout[0],
        #'col2_width': layout[1],
        #'col3_width': layout[2],
        #'col4_width': layout[3],
        'template': template,
        'theme': theme,
    }
    return options


def check_options(page):
    if page is not None and not hasattr(page, 'options'):
        return build_options(page)
    return {}
