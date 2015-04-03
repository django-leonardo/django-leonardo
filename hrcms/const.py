# -#- coding: utf-8 -#-

from django.utils.translation import ugettext_lazy as _

DEFAULT_WIDTH = 12

DEFAULT_CHOICE = 0

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
    (DEFAULT_CHOICE, _('none')),
    (1, _('break before')),
    (2, _('break after')),
)

BORDER_CHOICES = (
    (DEFAULT_CHOICE, _('no border')),
    (1, _('border')),
    (2, _('wide border')),
)

ALIGN_CHOICES = (
    (DEFAULT_CHOICE, _('auto')),
    (1, _('left')),
    (2, _('center')),
    (3, _('right')),
)

VERTICAL_ALIGN_CHOICES = (
    (DEFAULT_CHOICE, _('auto')),
    (1, _('top')),
    (2, _('middle')),
    (3, _('bottom')),
)

STYLE_CHOICES = (
    (DEFAULT_CHOICE, _('none')),
    (1, _('nested_box')),
    (2, _('padded')),
    (3, _('single box')),
    (4, _('box top')),
    (5, _('box middle')),
    (6, _('box bottom')),
)

# this wil be on the Page model
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
