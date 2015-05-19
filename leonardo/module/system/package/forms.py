from django.utils.translation import ugettext_lazy as _
from django_select2.fields import AutoSelect2TagField
from django_select2.views import NO_ERR_RESP
from leonardo import forms, messages

from .utils import update_all, get_widgets


class PluginSelectField(AutoSelect2TagField):
    """returns list of plugins from github group or pypi

    it's simple PoC
    """

    search_fields = ['tag__icontains', ]

    def get_field_values(self, value):
        raise Exception(value)
        return {'tag': value}

    def get_results(self, request, term, page, context):

        pkgs = get_widgets()

        res = [
            (
                repo.name,
                repo.name,
                {}
            )
            for repo in pkgs
        ]

        return NO_ERR_RESP, True, res


class PluginInstallForm(forms.SelfHandlingForm):

    plugins = PluginSelectField(label=_('Search plugin'))

    def handle(self, request, data):
        """PoC for installing plugins

        this support new abilities like an dynamic plugin install etc..
        """
        raise Exception(data)

        global ORG

        if ORG:
            for repo_id in data['plugins']:
                repo = ORG.get_repo(repo_id)
                raise Exception(repo)
        try:
            import github  # noqa
        except ImportError:
            messages.error(request, _(
                'For this functionality please run pip install PyGithub'))
        g = github.Github()

        raise Exception(data)
        try:
            messages.warning(
                request, _('Server going to down !'))
        except Exception as e:
            messages.error(request, str(e))
        else:
            return True
        return False
