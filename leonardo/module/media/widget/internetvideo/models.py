# -#- coding: utf-8 -#-

import re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from leonardo.module.web.models import Widget

PORTALS = (
    ('youtube', re.compile(r'youtube'), lambda url: {
     'v': re.search(r'[?&]v=([^#&]+)', url).group(1)}),
    ('vimeo', re.compile(r'vimeo'), lambda url: {
     'id': re.search(r'/(\d+)', url).group(1)}),
    ('sf', re.compile(r'sf\.tv'), lambda url: {
     'id': re.search(r'/([a-z0-9\-]+)', url).group(1)}),
)


class InternetVideoWidget(Widget):

    """
    Copy-paste a URL to youtube or vimeo into the text box, this content type
    will automatically generate the necessary embed code.

    Other portals aren't supported currently, but would be easy to add if anyone
    would take up the baton.
    """

    icon = "fa fa-youtube-square"

    video = models.URLField(_('video link'),
                            help_text=_('This should be a link to a youtube or vimeo video, i.e.: http://www.youtube.com/watch?v=zmj1rpzDRZ0'))

    def source(self, **kwargs):
        for portal, match, context_fn in PORTALS:
            if match.search(self.video):
                return portal
        return 'unknown'

    def source_id(self, **kwargs):
        for portal, match, context_fn in PORTALS:
            if match.search(self.video):
                return context_fn(self.video)
        return self.video

    class Meta:
        abstract = True
        verbose_name = _('internet video')
        verbose_name_plural = _('internet videos')
