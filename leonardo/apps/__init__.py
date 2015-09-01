
from __future__ import absolute_import

from leonardo.module.web.widget.application.models import ApplicationWidget
from leonardo.module.web.widget.application.reverse import (app_reverse,
                                                            app_reverse_lazy)

try:
    from feincms.views.decorators import standalone, unpack
    from feincms.content.application.models import permalink
except:
    from feincms.apps import standalone, permalink, unpack

from .leonardo import *

__all__ = (
    'ApplicationWidget',
    'app_reverse', 'app_reverse_lazy', 'permalink',
    'standalone', 'unpack',
)
