from horizon import conf


def leonardo(request):
    """
    Add LEONARDO_CONFIG to context
    """

    try:
        return {
           "LEONARDO_CONFIG": conf.HORIZON_CONFIG
        }
    except:
        return {}
