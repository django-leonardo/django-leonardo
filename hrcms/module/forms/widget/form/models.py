# -#- coding: utf-8 -#-

from django.db import models
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from form_designer.models import Form
from hrcms.models import Widget


class FormWidget(Widget):
    form = models.ForeignKey(Form, verbose_name=_('form'),
                             related_name='%(app_label)s_%(class)s_related')
    show_form_title = models.BooleanField(_('show form title'), default=True)
    success_message = models.TextField(
        _('success message'), blank=True, help_text=_("Optional custom message to display after valid form is submitted"))

    class Meta:
        abstract = True
        verbose_name = _('form')
        verbose_name_plural = _('forms')

    def process_valid_form(self, request, form_instance, **kwargs):
        """ Process form and return response (hook method). """
        process_result = self.form.process(form_instance, request)
        context = RequestContext(
            request, {
                'content': self,
                'message': self.success_message or process_result or u''})
        return render_to_string(self.template_name, context)

    def render_content(self, kwargs):
        request = kwargs['request']
        form_class = self.form.form()
        prefix = 'fc%d' % self.id

        if request.method == 'POST':
            form_instance = form_class(request.POST, prefix=prefix)

            if form_instance.is_valid():
                return self.process_valid_form(request, form_instance, **kwargs)
        else:
            form_instance = form_class(prefix=prefix)

        context = RequestContext(
            request, {'widget': self, 'form': form_instance})
        return render_to_string(self.template_name, context)
