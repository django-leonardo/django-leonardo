# -#- coding: utf-8 -#-
from django.utils.translation import ugettext_lazy as _

DEFAULT_WIDTH = 12

DEFAULT_CHOICE = 0

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
        'path': 'base/layout.html',
        'regions': (col3, header, footer, toolbar, preview, helper),
    },
    # |-------------------------------|
    # |  col1   |  col3    |  col2    |
    # | ---     | flexible | flexible |
    # |-------------------------------|
    {
        'title': _('2 same columns'),
        'key': 'layout_flex_flex',
        'path': 'base/layout.html',
        'regions': (col3_left, col2, header, footer, toolbar, preview, helper),
    },
    # |-------------------------------|
    # |  col1   |  col3     |  col2   |
    # | ---     | flexible  | fixed   |
    # |-------------------------------|
    {
        'title': _('2 columns right'),
        'key': 'layout_flex_fixed',
        'path': 'base/layout.html',
        'regions': (col3, col2, header, footer, toolbar, preview, helper),
    },
    # |-------------------------------|
    # |  col1   |  col3     |  col2   |
    # | fixed   | flexible  | ---     |
    # |-------------------------------|
    {
        'title': _('2 columns left'),
        'key': 'layout_fixed_flex',
        'path': 'base/layout.html',
        'regions': (col3, col1, header, footer, toolbar, preview, helper),
    },
    # |-------------------------------|
    # |  col1   |  col3     |  col2   |
    # | fixed   | flexible  | fixed   |
    # |-------------------------------|
    {
        'title': _('3 columns'),
        'key': 'layout_fixed_flex_fixed',
        'path': 'base/layout.html',
        'regions': (col3, col1, col2, header, footer, toolbar, preview, helper),
    },
    # |-------------------------------|
    # |  col1   |  col3     |  col2   |
    # |  flex   | flexible  |  flex   |
    # |-------------------------------|
    {
        'title': _('3 same columns'),
        'key': 'layout_flex_flex_flex',
        'path': 'base/layout.html',
        'regions': (col1, col3_center, col2, header, footer, toolbar, preview, helper),
    },
    # DEPRECATED
    {
        'title': _('Dashboard'),
        'key': 'dashboard',
        'path': 'layout/dashboard.html',
        'regions': (col1, col3_center, col2, header, footer, toolbar, preview, helper),
    },
    {
        'title': _('API'),
        'key': 'api',
        'path': 'rest_framework/api.html',
        'regions': (col1, col3_center, col2, header, footer, toolbar, preview, helper),
    },
)

PAGE_LAYOUT_CHOICES = (
    ('fixed', _('Fixed')),
    ('fluid', _('Fluid')),
    ('boxed', _('Boxed')),
)

WIDGET_LAYOUT_CHOICES = (
    ('inline', _('Inline')),
    ('fixed', _('Fixed')),
    ('fluid', _('Fluid')),
)

WIDGET_ALIGN_CHOICES = (
    ('left', _('Left')),
    ('center', _('Center')),
    ('right', _('Right')),
)

DISPLAY_SIZE_CHOICES = (
    ('xs', _('Extra small')),
    ('sm', _('Small')),
    ('md', _('Medium')),
    ('lg', _('Large')),
)

COLUMN_CHOICES = (
    (DEFAULT_CHOICE,  ' — '),
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
    (DEFAULT_WIDTH, _('12 cols')),
)

ROW_CHOICES = (
    (DEFAULT_CHOICE,   ' — '),
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
    (13, _('13 row')),
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

ALIGN_CHOICES = (
    (DEFAULT_CHOICE, _('auto')),
    (1, _('left')),
    (2, _('center')),
    (3, _('right')),
)

VERTICAL_ALIGN_CHOICES = (
    ('top', _('top')),
    ('middle', _('middle')),
    ('bottom', _('bottom')),
)
