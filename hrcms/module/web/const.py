# -#- coding: utf-8 -#-
from django.utils.translation import ugettext_lazy as _

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

COLUMN_CHOICES = (
    (0, u' — '),
    (1, _('1 col')),
    (2, _('2 cols')),
    (3, _('3 cols')),
    (4, _('4 cols')),
    (5, _('5 cols')),
    (6, _('6 cols')),
    (7, _('7 cols')),
    (8, _('8 cols')),
    (9, _('9 cols')),
    (10, _('10 cols')),
    (11, _('11 cols')),
    (12, _('12 cols')),
    (13, _('13 cols')),
    (14, _('14 cols')),
    (15, _('15 cols')),
    (16, _('16 cols')),
    (17, _('17 cols')),
    (18, _('18 cols')),
    (19, _('19 cols')),
    (20, _('20 cols')),
    (21, _('21 cols')),
    (22, _('22 cols')),
    (23, _('23 cols')),
    (24, _('24 cols')),
)

ROW_CHOICES = (
    (0, u' — '),
    (1, _('1 row')),
    (2, _('2 rows')),
    (3, _('3 rows')),
    (4, _('4 rows')),
    (5, _('5 rows')),
    (6, _('6 rows')),
    (7, _('7 rows')),
    (8, _('8 rows')),
    (9, _('9 rows')),
    (10, _('10 rows')),
    (11, _('11 rows')),
    (12, _('12 rows')),
    (13, _('13 rows')),
    (14, _('14 rows')),
    (15, _('15 rows')),
    (16, _('16 rows')),
    (17, _('17 rows')),
    (18, _('18 rows')),
    (19, _('19 rows')),
    (20, _('20 rows')),
    (21, _('21 rows')),
    (22, _('22 rows')),
    (23, _('23 rows')),
    (24, _('24 rows')),
)

CLEAR_CHOICES = (
    ('', _('none')),
    ('f', _('break before')),
    ('l', _('break after')),
)

BORDER_CHOICES = (
    ('0', _('no border')),
    ('1', _('border')),
    ('2', _('wide border')),
)

ALIGN_CHOICES = (
    ('a', _('auto')),
    ('l', _('left')),
    ('c', _('center')),
    ('r', _('right')),
)

VERTICAL_ALIGN_CHOICES = (
    ('a', _('auto')),
    ('t', _('top')),
    ('m', _('middle')),
    ('b', _('bottom')),
)

STYLE_CHOICES = (
    ('', _('none')),
    ('nested_box', _('nested_box')),
    ('padded', _('padded')),
    ('boxed', _('single box')),
    ('boxed-top', _('box top')),
    ('boxed-middle', _('box middle')),
    ('boxed-bottom', _('box bottom')),
)

DEFAULT_DISPLAY_OPTIONS = {
    'label': None,
    'template_name': 'default',
    'style': None,
    'size': [24, 0],
    'align': ["a", "a"],
    'padding': [0, 0, 0, 0],
    'margin': [0, 0, 0, 0],
    'visible': True,
    'border': None,
    'clear': None,
    'last': False,
}
