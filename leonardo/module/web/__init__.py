
import logging
from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _
from .widget import *


default_app_config = 'leonardo.module.web.WebConfig'

LOG = logging.getLogger(__name__)


class Default(object):

    optgroup = 'Web'

    urls_conf = 'leonardo.module.web.urls'

    @property
    def page_extensions(self):

        return [
            'feincms.module.page.extensions.excerpt',
            'feincms.module.page.extensions.relatedpages',
            'feincms.module.page.extensions.navigation',
            'feincms.module.page.extensions.sites',
            'feincms.module.page.extensions.symlinks',
            'feincms.module.page.extensions.titles',
            'leonardo.extensions.seo',
            'leonardo.extensions.datepublisher',
            'leonardo.extensions.translations',
            'leonardo.extensions.changedate',
            'leonardo.extensions.ct_tracker',
            'leonardo.extensions.featured'
        ]

    @property
    def middlewares(self):
        return [
            'leonardo.module.web.middlewares.web.WebMiddleware',
            'leonardo.module.web.middlewares.horizon.HorizonMiddleware',
        ]

    channel_routing = [
        ('leonardo.module.web.widgets.routing.channel_routing',
         {'path': r"^/widgets"})
    ]

    @property
    def apps(self):

        INSTALLED_APPS = []

        # optionaly enable sorl.thumbnail
        try:
            import sorl  # noqa
            INSTALLED_APPS += ['sorl.thumbnail']
        except Exception:
            pass

        # optionaly enable easy_thumbnails
        try:
            import easy_thumbnails  # noqa
            INSTALLED_APPS += ['easy_thumbnails']
        except Exception:
            pass

        # optionaly enable constance
        try:
            import constance
        except ImportError:
            pass
        else:
            INSTALLED_APPS += ['constance',
                               'constance.backends.database']

        return INSTALLED_APPS + [
            'feincms',
            'mptt',
            'crispy_forms',
            'floppyforms',

            'dbtemplates',
            'leonardo.module',

            'feincms.module.page',  # noqa

            'leonardo.module.web',

            'markupfield',
        ]

    @property
    def context_processors(self):
        """return WEB Conent Type Processors
        """
        return [
            'leonardo.module.web.processors.page.add_page_if_missing',
            'leonardo.module.web.processors.config.leonardo',
        ]

    @property
    def widgets(self):
        return [
            'leonardo.module.web.models.ApplicationWidget',
            'leonardo.module.web.models.SiteHeadingWidget',
            ('leonardo.module.web.models.FeedReaderWidget', {
             'dummy': 'dummy'}),
            'leonardo.module.web.models.MarkupTextWidget',
            'leonardo.module.web.models.HtmlTextWidget',
            'leonardo.module.web.models.PageTitleWidget',
            'leonardo.module.web.models.IconWidget',
        ]

    plugins = [
        ('leonardo.module.web.apps.horizon', _('Horizon'))
    ]

    js_files = [
        'js/lib/wow.min.js'
    ]

    angular_modules = ['ngFitText']

    css_files = [
        'css/lib/animate.css',
        'css/lib/select2.css',
    ]

    css_files = [
        'css/lib/animate.css',
        'css/lib/select2.css',
        'css/lib/lightbox.css',
    ]

    config = {
        'META_KEYWORDS': ('', _('Site specific meta keywords')),
        'META_DESCRIPTION': ('', _('Site specific meta description')),
        'META_TITLE': ('', _('Site specific meta title')),
        'DEBUG': (True, _('Debug mode')),
        'FAVICON_PATH': ('/static/img/favicon.ico', _('Favicon path')),
        'DEFAULT_FROM_EMAIL': ('webmaster@localhost', 'Default from email.'),
    }

    # Example of custom field
    additional_fields = {
        'yes_no_null_select': ['django.forms.fields.ChoiceField',
                               {
                                   'widget': 'django.forms.Select',
                                   'choices': (("-----", None), ("yes", "Yes"), ("no", "No"))
                               }],
    }

    page_actions = ['base/page/_actions.html']
    widget_actions = ['base/widget/_actions.html']


class WebConfig(AppConfig, Default):
    name = 'leonardo.module.web'
    verbose_name = "CMS"

    def ready(self):

        # register signals
        from leonardo.module.web.signals import save as template_save
        from dbtemplates.models import Template

        Template.save = template_save

        from leonardo.module.web.models import Page
        # override page defaults without migrations
        Page._meta.get_field('template_key').default = 'layout_flex_flex_flex'

        from django.db.models.signals import post_save
        from .widgets.reciever import update_widget_reciever
        post_save.connect(update_widget_reciever,
                          dispatch_uid="update_widgets")

default = Default()
