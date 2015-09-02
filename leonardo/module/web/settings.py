
from __future__ import absolute_import

from .widget import *

from .const import *
from .models import Page


FEINCMS_REVERSE_MONKEY_PATCH = False

LEONARDO_FRONTEND_EDITING = True

Page.register_templates(*PAGE_TEMPLATES)

THUMBNAIL_DEBUG = True
