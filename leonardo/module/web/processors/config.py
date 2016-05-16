from horizon import conf
from leonardo import leonardo as main


class ContextConfig(dict):

    '''Lazy access for all config from templates
    This object takes request and provide it to
    functions directly when is need it in templates
    Simple support for feature toggle

    Example:

        LEONARDO_EXTRA_CONTEXT = {
            'is_feature_enabled': lambda request: if request.user.is..
        }
        then use it in templates
        {% if LEONARDO_CONFIG.is_feature_enabled %}
    '''

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ContextConfig, self).__init__(*args, **kwargs)

    def __getattr__(self, attr):

        if attr == 'request':
            return self.get(attr)

        if attr in conf.HORIZON_CONFIG:
            return conf.HORIZON_CONFIG.get(attr)

        # support calling custom functions from context
        # and directly access to extra context
        if attr in main.config.extra_context:
            func = main.config.extra_context.get(attr, None)

            if callable(func):
                return func(self.request)
            else:
                return func

        return getattr(main.config, attr, None)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def leonardo(request):
    """
    Add LEONARDO_CONFIG to context
    """

    try:
        return {
            "LEONARDO_CONFIG": ContextConfig(request)
        }
    except:
        return {}
