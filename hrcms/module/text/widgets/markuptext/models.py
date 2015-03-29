from django.db import models
from django.utils.translation import ugettext_lazy as _
from markupfield.fields import MarkupField
from hrcms.module.boardie.models import WidgetMixin
from hrcms.module.boardie.forms import AngularTextInput, AngularSelect, AngularTextarea, AngularRadioButton
from crispy_forms.layout import Layout, TabHolder, Tab

class MarkupTextContent(models.Model):
    """
    Content which can be used to input HTMLed text into the dashboard.
    """
    text = MarkupField(verbose_name=_('text'), blank=True, default=_('Empty text'), default_markup_type='ReST')

    class Meta:
        abstract = True
        verbose_name = _("markup text")
        verbose_name_plural = _("markup texts")

class MarkupTextWidget(WidgetMixin, MarkupTextContent):
    """
    Widget which can be used to input HTMLed text into the dashboard.
    """

    @classmethod
    def form_fields(self):
        return [
            'name',
            'width',
            'height',
            'update_interval_length',
            'update_interval_unit',
            'text'
        ]

    @classmethod
    def form_widgets(self):
        return {
            'name': AngularTextInput(attrs={'autofocus': True}),
            'width': AngularSelect,
            'height': AngularSelect,
            'update_interval_length': AngularTextInput,
            'update_interval_unit': AngularRadioButton,
            'text': AngularTextarea,
        }

    @classmethod
    def form_layout(self):
        return TabHolder(
            Tab('Text',
                'name',
                'text',
            ),
            Tab('Size',
                'width',
                'height',
                'update_interval_length',
                'update_interval_unit',
            ),
        )

    def widget_data(self, request):
        data = {
            'rendered_text': self.text.rendered,
            'markup_type': self.text_markup_type
        }
        return data

    class Meta:
        abstract = True
        verbose_name = _("markup text")
        verbose_name_plural = _("markup texts")

    def save(self, *args, **kwargs):
        if self.text == '' or self.text == None:
            self.text = _('Empty text')
        super(MarkupTextWidget, self).save(*args, **kwargs)
