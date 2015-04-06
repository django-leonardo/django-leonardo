# -#- coding: utf-8 -#-

from django import forms
from django.db import models
from django.template import RequestContext, Template
from django.template.loader import render_to_string
from django.utils.translation import ugettext as __
from django.utils.translation import ugettext_lazy as _
from feincms.admin.item_editor import ItemEditorForm
from leonardo.module.web.models import Widget


class DjangoTemplateWidgetAdminForm(ItemEditorForm):
    template = forms.CharField(
        widget=forms.Textarea, required=False, label=_('template'))

    def __init__(self, *args, **kwargs):
        super(DjangoTemplateWidgetAdminForm, self).__init__(*args, **kwargs)
        self.fields['template'].widget.attrs.update(
            {'class': 'item-djangotemplate'})


class DjangoTemplateWidget(Widget):
    form = DjangoTemplateWidgetAdminForm
    feincms_item_editor_form = DjangoTemplateWidgetAdminForm

    feincms_item_editor_includes = {
        'head': ['admin/widget/djangotemplate/init_ace.html'],
    }

    #template = models.TextField(verbose_name=_("template"),)

    class Meta:
        abstract = True
        verbose_name = _("django template")
        verbose_name_plural = _("django templates")

    def save(self, *args, **kwargs):
        if self.template == '':
            self.template = __('Empty template')
        super(DjangoTemplateWidget, self).save(*args, **kwargs)

    def render_template(self, kwargs):
        template = Template(self.template)
        context = RequestContext(kwargs['request'])
        return template.render(context)

    def render_content(self, options):
        return render_to_string(self.template_name, {
            'widget': self,
            'options': options,
            'request': options['request'],
            'content': self.render_template(options)
        })
