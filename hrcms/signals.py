# -#- coding: utf-8 -#-

from hrcms.module.web.models import check_options
from feincms.module.page.models import Page


def page_check_options(sender, **kwargs):
    instance = kwargs.get('instance')

    options = check_options(instance)
    if options:
        instance.options = options
        #raise Exception(instance.attrs)


def test(sender, **kwargs):
    instance = kwargs.get('instance')
    page = Page.objects.get(pk=instance.id)

    #raise Exception(page.get('options'))
