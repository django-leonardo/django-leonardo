
from django.apps import AppConfig

from django.utils.functional import lazy
from django.utils import six


class LeonardoConfig(AppConfig):
    name = 'leonardo'
    verbose_name = "Leonardo"

    def ready(self):

        from django.template import defaulttags

        # monkey path url tag
        from leonardo.utils.urlresolvers import render
        defaulttags.URLNode.render = render

        # monkey path django reverse
        from django.core import urlresolvers
        from leonardo.module.web.widget.application.reverse import reverse

        urlresolvers.reverse = reverse
        urlresolvers.reverse_lazy = lazy(reverse, six.text_type)

        # path settings for support functionality without hell
        # this needs restart for propagation some keys
        from horizon.conf import HORIZON_CONFIG
        from horizon import conf as horizon_conf
        try:
            # optionaly copy all live configuration to horizon/leonardo
            from constance import config
            from django.conf import settings

            for k in dir(config):
                if k not in HORIZON_CONFIG:
                    HORIZON_CONFIG[k] = getattr(config, k)
        except:
            pass
        else:
            horizon_conf.HORIZON_CONFIG = HORIZON_CONFIG

        try:
            # optionaly copy all live configuration to main settings
            from constance import config
            from django.conf import settings

            for k in dir(config):
                setattr(settings, k, getattr(config, k))
        except Exception:
            # in some environment may failed
            # use optionaly strategy
            pass

        # use our debug 404 for quick build scaffold of site
        try:
            from django.views import debug
            from leonardo.views.debug import technical_404_response
            debug.technical_404_response = technical_404_response
        except:
            pass
