from django.utils.translation import ugettext_lazy as _
from django_select2.fields import AutoSelect2TagField
from django_select2.views import NO_ERR_RESP
from leonardo import forms, messages

from .utils import pip_install, update_all


class PluginSelectField(AutoSelect2TagField):

    """returns list of plugins from github group or pypi

    it's simple PoC !
    """

    search_fields = ['tag__icontains', ]

    def get_field_values(self, value):
        raise Exception(value)
        return {'tag': value}

    def get_results(self, request, term, page, context):

        pkgs = update_all()

        res = [
            (
                repo.name,
                repo.name,
                {}
            )
            for repo in pkgs if term in repo.name
        ]

        return NO_ERR_RESP, True, res


class PluginInstallForm(forms.SelfHandlingForm):
    """simple form for installing packages

    this support new abilities like an dynamic plugin install etc..
    """

    packages = PluginSelectField(label=_('Search packages'))

    reload_server = forms.BooleanField(
        label=_('Reload Server'), initial=False,
        required=False,
        help_text=_('Warning: this kill this Leonardo instance !!!\
                    For successfull reload must be run under Supervisor !\
                    You may lost your data !'),)

    def __init__(self, *args, **kwargs):
        super(PluginInstallForm, self).__init__(*args, **kwargs)

        self.helper.layout = forms.Layout(
            forms.Accordion('', 'packages',
                            forms.AccordionGroup(
                                _('Advanced options'),
                                'reload_server',
                                )
                            ),
        )

    def handle(self, request, data):

        kwargs = data
        kwargs['request'] = request
        try:
            pip_install(**kwargs)
        except Exception as e:
            messages.error(request, str(e))
        else:
            return True
        return False
