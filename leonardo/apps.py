
from django.apps import AppConfig

from django.db.models.signals import pre_save, post_save


class LeonardoConfig(AppConfig):
    name = 'leonardo'
    verbose_name = "Leonardo"

    def ready(self):

        from django.template import defaulttags

        # monkey path url tag
        from leonardo.templatetags.url import render
        defaulttags.URLNode.render = render

        # monkey path django reverse
        from django.core import urlresolvers
        from leonardo.module.web.widget.application.reverse import reverse

        urlresolvers.reverse = reverse
