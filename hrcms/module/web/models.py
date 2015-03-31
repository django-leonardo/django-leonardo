# -#- coding: utf-8 -#-

from django.utils.translation import ugettext_lazy as _

from hrcms.module.web.config import WEB_GROUP

from south.modelsinspector import add_introspection_rules

add_introspection_rules([], ["^webcms\.utils\.models\.JSONField"])
add_introspection_rules([], ["^markupfield\.fields\.MarkupField"])

PAGE_REGIONS_LIST = (
    'col3', 'col1', 'col2', 'header', 'footer', 'toolbar', 'preview', 'helper',)

PAGE_REGIONS = (
    ('col3', _('Content')),
    ('col1', _('Left sidebar')),
    ('col2', _('Right sidebar')),
    ('header', _('Header')),
    ('footer', _('Footer')),
    ('toolbar', _('Toolbar')),
    ('preview', _('Preview')),
    ('helper', _('Helper'))
)

col1 = ('col1', _('Left column'), 'inherited')
col2 = ('col2', _('Right column'), 'inherited')
col3 = ('col3', _('Main content'))
col3_center = ('col3', _('Center column'))
col3_left = ('col3', _('Left column'))
header = ('header', _('Header'), 'inherited')
content = ('content', _('Content'))
footer = ('footer', _('Footer'), 'inherited')
toolbar = ('toolbar', _('Toolbar'), 'inherited')
preview = ('preview', _('Preview'))
helper = ('helper', _('Helper'))

PAGE_TEMPLATES = (
    # |-------------------------------|
    # |  col1   |  col3     |  col2   |
    # | ---     | flexible  | ---     |
    # |-------------------------------|
    {
        'title': _('1 column'),
        'key': 'layout_flex',
        'path': 'layout/page_flex.html',
        'regions': (col3, header, footer, toolbar, preview, helper),
    },
    # |-------------------------------|
    # |  col1   |  col3    |  col2    |
    # | ---     | flexible | flexible |
    # |-------------------------------|
    {
        'title': _('2 same columns'),
        'key': 'layout_flex_flex',
        'path': 'layout/page_flex_flex.html',
        'regions': (col3_left, col2, header, footer, toolbar, preview, helper),
    },
    # |-------------------------------|
    # |  col1   |  col3     |  col2   |
    # | ---     | flexible  | fixed   |
    # |-------------------------------|
    {
        'title': _('2 columns right'),
        'key': 'layout_flex_fixed',
        'path': 'layout/page_flex_fixed.html',
        'regions': (col3, col2, header, footer, toolbar, preview, helper),
    },
    # |-------------------------------|
    # |  col1   |  col3     |  col2   |
    # | fixed   | flexible  | ---     |
    # |-------------------------------|
    {
        'title': _('2 columns left'),
        'key': 'layout_fixed_flex',
        'path': 'layout/page_fixed_flex.html',
        'regions': (col3, col1, header, footer, toolbar, preview, helper),
    },
    # |-------------------------------|
    # |  col1   |  col3     |  col2   |
    # | fixed   | flexible  | fixed   |
    # |-------------------------------|
    {
        'title': _('3 columns'),
        'key': 'layout_fixed_flex_fixed',
        'path': 'layout/page_fixed_flex_fixed.html',
        'regions': (col3, col1, col2, header, footer, toolbar, preview, helper),
    },
    # |-------------------------------|
    # |  col1   |  col3     |  col2   |
    # |  flex   | flexible  |  flex   |
    # |-------------------------------|
    {
        'title': _('3 same columns'),
        'key': 'layout_flex_flex_flex',
        'path': 'layout/page_flex_flex_flex.html',
        'regions': (col1, col3_center, col2, header, footer, toolbar, preview, helper),
    },
    {
        'title': _('Void'),
        'key': 'layout_void',
        'path': 'layout/page_void.html',
        'regions': (col1, col3_center, col2, header, footer, toolbar, preview, helper),
    },
)

TEMPLATE_LAYOUTS = {
    'layout_flex': (0, 0, 24, 0),
    'layout_flex_flex': (0, 12, 12, 0),
    'layout_flex_fixed': (0, 6, 18, 0),
    'layout_fixed_flex': (6, 0, 18, 0),
    'layout_fixed_flex_fixed': (6, 6, 12, 0),
    'layout_flex_flex_flex': (8, 8, 8, 0),
    'layout_void': (6, 6, 6, 6),
}

from feincms.module.page.models import Page
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