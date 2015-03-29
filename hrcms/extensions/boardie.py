"""
Add an dashboard fields to the page.
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _
from feincms import extensions

THEME_CHOICES = (
    ('default', _('Default theme')),
    #    ('amelia', _('Amelia')),
    ('cosmo', _('Cosmo')),
    ('cyborg', _('Cyborg')),
    #    ('slate', _('Slate')),
    #    ('superhero', _('Superhero')),
    ('united', _('United')),
)


class Board(extensions.Extension):

    def handle_model(self):
        self.model.add_to_class('board_theme', models.CharField(_('dashboard theme'), max_length=100, blank=True,
                                                                help_text=_('Dashboard theme for browser window.'), choices=THEME_CHOICES, default="default"))
        self.model.add_to_class('board_locked', models.BooleanField(_('locked'),
                                                                    help_text=_('Is dashboard locked for editing?'), default=False))
        self.model.add_to_class('board_public', models.BooleanField(_('public'),
                                                                    help_text=_('Is dashboard open for public viewing?'), default=False))
        self.model.add_to_class('board_width', models.IntegerField(_('Board width'), default=1920,
                                                                   help_text=_('Width in pixels of the whole dashboard.')))
        self.model.add_to_class('board_height', models.IntegerField(_('Board height'), default=1080,
                                                                    help_text=_('Height in pixels of the whole dashboard.')))
        self.model.add_to_class('widget_width', models.IntegerField(_('Widget width'), default=220,
                                                                    help_text=_('Width in pixels of a single widget.')))
        self.model.add_to_class('widget_height', models.IntegerField(_('Widget height'), default=220,
                                                                     help_text=_('Height in pixels of a single widget.')))
        self.model.add_to_class('widget_max_width', models.IntegerField(_('Widget max. width'), default=6,
                                                                        help_text=_('The maximum number of columns that a widget can span.')))
        self.model.add_to_class('widget_max_height', models.IntegerField(_('Widget max. height'), default=6,
                                                                         help_text=_('The maximum number of rows that a widget can span.')))
        self.model.add_to_class('widget_margin_vertical', models.IntegerField(_('Widget vertical margins'), default=10,
                                                                              help_text=_('Vertical margins in pixels of a single widget.')))
        self.model.add_to_class('widget_margin_horizontal', models.IntegerField(_('Widget horizontal margins'), default=10,
                                                                                help_text=_('Horizontal margins in pixels of a single widget.')))

    def handle_modeladmin(self, modeladmin):
        """
        modeladmin.add_extension_options(_('Titles'), {
            'fields': ('_content_title', '_page_title'),
            'classes': ('collapse',),
        })
        modeladmin.add_extension_options((_('Dashboard options'), {
            'fields': ('board_width', 'board_height', 'board_theme', 'board_locked', 'board_public',),
            #        'classes': ('collapse',),
        }))

        modeladmin.add_extension_options((_('Widget options'), {
            'fields': ('widget_margin_vertical', 'widget_margin_horizontal', 'widget_width', 'widget_height', 'widget_max_width', 'widget_max_height',),
            #        'classes': ('collapse',),
        }))
        """
