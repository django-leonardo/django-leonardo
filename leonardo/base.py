

class Leonardo(object):

    def get_app_modules(self, apps):
        """return imported leonardo modules
        return {'web': web.module}
        """
        from django.utils.importlib import import_module
        from django.utils.module_loading import module_has_submodule
        modules = {}

        # Try importing a modules from the module package
        package_string = '.'.join(['leonardo', 'module'])

        for app in apps:
            try:
                # check if is not full app
                _app = import_module(app)
            except ImportError:
                _app = False
            if not _app:
                try:
                    # check if is not leonardo_module
                    _app = import_module('leonardo_module_{}'.format(app))
                except ImportError:
                    _app = False

            if module_has_submodule(import_module(package_string), app) or _app:
                if _app:
                    mod = _app
                else:
                    mod = import_module('.{0}'.format(app), package_string)
                modules[app] = mod
        return modules


leonardo = Leonardo()
