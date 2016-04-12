
from app_loader.config import Config, MasterConfig
from app_loader.utils import merge
from leonardo.conf.spec import CONF_SPEC, DJANGO_CONF
from leonardo.utils.versions import get_versions


class ModuleConfig(Config):

    """Simple Module Config Object
    encapsulation of dot access dictionary

    use dictionary as constructor

    """

    def get_value(self, key, values):
        '''Accept key of propery and actual values'''
        return merge(values, self.get_property(key))

    def get_property(self, key):
        """Expect Django Conf property"""
        _key = DJANGO_CONF[key]
        return getattr(self, _key, CONF_SPEC[_key])

    @property
    def module_name(self):
        """Module name from module if is set"""
        if hasattr(self, "module"):
            return self.module.__name__
        return None

    @property
    def name(self):
        """Distribution name from module if is set"""
        if hasattr(self, "module"):
            return self.module.__name__.replace('_', '-')
        return None

    @property
    def version(self):
        """return module version"""
        return get_versions([self.module_name]).get(self.module_name, None)

    @property
    def latest_version(self):
        """return latest version if is available"""
        from leonardo_system.pip import check_versions
        return check_versions(True).get(self.name, None).get('new', None)

    @property
    def needs_migrations(self):
        """Indicates whater module needs migrations"""
        # TODO(majklk): also check models etc.
        if len(self.widgets) > 0:
            return True
        return False

    @property
    def needs_sync(self):
        """Indicates whater module needs templates, static etc."""

        affected_attributes = [
            'css_files', 'js_files',
            'scss_files', 'widgets']

        for attr in affected_attributes:
            if len(getattr(self, attr)) > 0:
                return True
        return False

    def set_module(self, module):
        """Just setter for module"""
        setattr(self, "module", module)


class LeonardoConfig(MasterConfig):

    @property
    def is_websocket_enabled(self):
        '''Reffers if channels is installed'''
        try:
            import leonardo_channels
        except ImportError:
            return False
        else:
            return True
