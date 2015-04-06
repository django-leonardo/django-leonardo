# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from livesettings import ConfigurationGroup, PositiveIntegerValue, MultipleStringValue, StringValue, LongStringValue, BooleanValue, config_register, config_register_list

MEDIA_GROUP = ConfigurationGroup('MEDIA', _('Media settings'), ordering = 110)

config_register(
    BooleanValue(MEDIA_GROUP,
        'SYNC_FOLDERS',
        description=_("Synchronise folders"),
        help_text=_("If yes, every folder will be synced with a Media Category."),
        default=False
    )
)

config_register(
    StringValue(MEDIA_GROUP,
        'THUMB_SMALL_GEOM',
        description=_('small thumb geomerty'),
        default = '64x64',
        help_text = _('Geometry of small thumbnails. I.e.: "400x50" or "x90"')
    )
)

config_register(
    LongStringValue(MEDIA_GROUP,
        'THUMB_SMALL_OPTIONS',
        description=_('small thumb options'),
        default = '',
        help_text = _('Additional options for small thumnais.')
    )
)

config_register(
    StringValue(MEDIA_GROUP,
        'THUMB_MEDIUM_GEOM',
        description=_('medium thumb geomerty'),
        default = '128x128',
        help_text = _('Geometry of medium thumbnails. I.e.: "400x50" or "x90"')
    )
)

config_register(
    LongStringValue(MEDIA_GROUP,
        'THUMB_MEDIUM_OPTIONS',
        description=_('medium thumb options'),
        default = '',
        help_text = _('Additional options for medium thumnais.')
    )
)

config_register(
    StringValue(MEDIA_GROUP,
        'THUMB_LARGE_GEOM',
        description=_('large thumb geomerty'),
        default = '192x192',
        help_text = _('Geometry of large thumbnails. I.e.: "400x50" or "x90"')
    )
)

config_register(
    LongStringValue(MEDIA_GROUP,
        'THUMB_LARGE_OPTIONS',
        description=_('large thumb options'),
        default = '',
        help_text = _('Additional options for large thumbnais.')
    )
)
