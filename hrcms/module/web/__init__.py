
#default_app_config = 'hrcms.module.web.apps.WebAppConfig'

VERSION = (0, 1, 1,)
__version__ = '.'.join(map(str, VERSION))


class Default(object):

    @property
    def middlewares(self):
        return [
            'hrcms.module.web.middleware.WebMiddleware',
        ]

    @property
    def apps(self):
        return [
            'markitup',
            'feincms',
            'mptt',

            'hrcms.module',

            'feincms.module.page',
            'feincms.content.application',
            #'feincms.content.comments',

            #'hrcms.module.nav',
            #'hrcms.module.lang',
            'hrcms.module.web',
            #'hrcms.module.forms',
            #'hrcms.module.boardie',
            'form_designer',
            'django_remote_forms',
        ]

    @property
    def ctp(self):
        """return WEB Conent Type Processors
        """
        return [
            'hrcms.module.web.processors.add_page_if_missing',
        ]

default = Default()