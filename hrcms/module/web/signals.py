# -#- coding: utf-8 -#-

from .models import check_options #, Page


def page_check_options(sender, **kwargs):
    instance = kwargs.get('instance')

    options = check_options(instance)
    if options:
        instance.options = options
        #raise Exception(instance.attrs)
