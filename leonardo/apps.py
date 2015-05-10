
from django.apps import AppConfig

from django.utils.functional import lazy
from django.utils import six


class LeonardoConfig(AppConfig):
    name = 'leonardo'
    verbose_name = "Leonardo"

    def ready(self):

        from django.template import defaulttags

        # monkey path url tag
        from leonardo.utils.urlresolvers import render
        defaulttags.URLNode.render = render

        # monkey path django reverse
        from django.core import urlresolvers
        from leonardo.module.web.widget.application.reverse import reverse

        urlresolvers.reverse = reverse
        urlresolvers.reverse_lazy = lazy(reverse, six.text_type)
