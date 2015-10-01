
default_app_config = 'leonardo.apps.LeonardoConfig'

__import__('pkg_resources').declare_namespace(__name__)


try:
    from leonardo.base import leonardo  # noqa
except ImportError:
    import warnings

    def simple_warn(message, category, filename, lineno, file=None, line=None):
        return '%s: %s' % (category.__name__, message)

    msg = ("Could not import Leonardo dependencies. "
           "This is normal during installation.\n")
    warnings.formatwarning = simple_warn
    warnings.warn(msg, Warning)
