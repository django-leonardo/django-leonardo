from horizon import conf
from leonardo import leonardo as main


class ContextConfig(dict):

    '''Lazy access for all config from templates
    '''

    def __getattr__(self, attr):

        if attr in conf.HORIZON_CONFIG:
            return conf.HORIZON_CONFIG.get(attr)

        return getattr(main.config, attr, None)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

context_config = ContextConfig()


def leonardo(request):
    """
    Add LEONARDO_CONFIG to context
    """

    try:
        return {
            "LEONARDO_CONFIG": context_config
        }
    except:
        return {}
