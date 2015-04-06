# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from livesettings import ConfigurationGroup, PositiveIntegerValue, MultipleStringValue, StringValue, LongStringValue, BooleanValue, config_register, config_register_list

WEB_GROUP = ConfigurationGroup('WEB', _('Web Settings'), ordering = 100)

config_register(
    LongStringValue(WEB_GROUP,
        'META_KEYWORDS',
        description=_('meta keywords'),
        default = '',
        help_text = _('Default meta keywords. If you have multilingual site, use keywords in all languages.'))
)

config_register(
    LongStringValue(WEB_GROUP,
        'META_DESCRIPTION',
        description=_('meta description'),
        default = '',
        help_text = _('Default description of the site. If you have multilingual site, write description in all languages.'))
)

config_register(
    StringValue(WEB_GROUP,
        'META_TITLE',
        description=_("title of the site"),
        default = 'WebCSM Project',
        help_text = _("Title of the site to be shown in browser's title bar."))
)

config_register(
    BooleanValue(WEB_GROUP,
        'UNDER_CONSTRUCTION',
        description=_("Under construction"),
        help_text=_("If yes, there will be just Under Construction notice instead of web."),
        default=False
    )
)

config_register(
    BooleanValue(WEB_GROUP,
        'IS_PRIVATE',
        description=_("Is private"),
        help_text=_("If yes, there will be just Login screen instead of web for anonymous users."),
        default=False
    )
)

