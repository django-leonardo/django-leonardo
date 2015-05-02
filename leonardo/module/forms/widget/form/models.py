# -#- coding: utf-8 -#-

from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _
from form_designer.models import FormContent
from leonardo.module.web.models import Widget


class FormWidget(Widget, FormContent):

    class Meta:
        abstract = True
        verbose_name = _('form')
        verbose_name_plural = _('forms')

    def render(self, request, **kwargs):
        form_class = self.form.form()
        prefix = 'fc%d' % self.id
        formcontent = request.POST.get('_formcontent')

        if request.method == 'POST' and (
                not formcontent or formcontent == smart_text(self.id)):
            form_instance = form_class(request.POST, prefix=prefix)

            if form_instance.is_valid():
                return self.process_valid_form(
                    request, form_instance, **kwargs)
        else:
            form_instance = form_class(prefix=prefix)

        context = RequestContext(
            request, {'widget': self, 'form': form_instance})
        return render_to_string(self.get_template_name, context)
