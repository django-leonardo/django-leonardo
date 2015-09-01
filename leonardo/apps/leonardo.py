
from __future__ import absolute_import

from django.apps import AppConfig

from django.utils.functional import lazy
from django.utils import six


class LeonardoConfig(AppConfig):
    name = 'leonardo'
    verbose_name = "Leonardo"

    def ready(self):

        from django.conf import settings
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

            for k in dir(config):
                if k not in HORIZON_CONFIG:
                    HORIZON_CONFIG[k] = getattr(config, k)
        except:
            pass
        else:
            horizon_conf.HORIZON_CONFIG = HORIZON_CONFIG

        # use our debug 404 for quick build scaffold of site
        try:
            from django.views import debug
            from leonardo.views.debug import technical_404_response
            debug.technical_404_response = technical_404_response
        except:
            pass

        # now we patch all models with absolute url overrides
        # this is important because Django path get_absolute_url when model
        # is imported ! this behaviour breaks our strategy
        from django.db.models.loading import get_model
        from django.conf import settings
        from django.utils.importlib import import_module  # noqa

        for model, method in six.iteritems(settings.ABSOLUTE_URL_OVERRIDES):
            try:
                mod_name = model.split('.')[0]
                model_cls =  get_model(mod_name, model.split('.')[-1])
                if callable(method):
                    _method = method
                else:
                    _mod = import_module(".".join(method.split('.')[:-1]))
                    _method = getattr(_mod, method.split('.')[-1])

                setattr(model_cls, 'get_absolute_url', _method)

            except Exception as e:
                raise e

        # patch compress
        from leonardo.utils.compress_patch import compress_monkey_patch
        compress_monkey_patch()
