# -#- coding: utf-8 -#-

from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.forms.util import ErrorList
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from feincms import settings
#from feincms.admin.item_editor import ItemEditorForm, FeinCMSInline
from feincms.utils import get_object
from leonardo.module.web.models import Widget
from leonardo.module.web.widgets.forms import WidgetUpdateForm


class HtmlTextWidgetAdminForm(WidgetUpdateForm):
    text = forms.CharField(
        widget=forms.Textarea(), max_length=9999, required=False, label=_('text'))

    class Meta:

        fields = ('text',)
        widgets = {'template_name': forms.widgets.Select(choices=[])}

    def __init__(self, *args, **kwargs):
        super(HtmlTextWidgetAdminForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'item-richtext'})


    #: If FEINCMS_TIDY_ALLOW_WARNINGS_OVERRIDE allows, we'll convert this into
    # a checkbox so the user can choose whether to ignore HTML validation
    # warnings instead of fixing them:
    seen_tidy_warnings = forms.BooleanField(
        required=False,
        label=_("HTML Tidy"),
        help_text=_("Ignore the HTML validation warnings"),
        widget=forms.HiddenInput
    )

    def clean(self):
        cleaned_data = super(HtmlTextWidgetAdminForm, self).clean()

        if settings.FEINCMS_TIDY_HTML:
            text, errors, warnings = get_object(
                settings.FEINCMS_TIDY_FUNCTION)(cleaned_data['text'])

            # Ick, but we need to be able to update text and
            # seen_tidy_warnings:
            self.data = self.data.copy()

            # We always replace the HTML with the tidied version:
            cleaned_data['text'] = text
            self.data['%s-text' % self.prefix] = text

            if settings.FEINCMS_TIDY_SHOW_WARNINGS and (errors or warnings):
                if settings.FEINCMS_TIDY_ALLOW_WARNINGS_OVERRIDE:
                    # Convert the ignore input from hidden to Checkbox so the
                    # user can change it:
                    self.fields[
                        'seen_tidy_warnings'].widget = forms.CheckboxInput()

                if errors or not (settings.FEINCMS_TIDY_ALLOW_WARNINGS_OVERRIDE and cleaned_data['seen_tidy_warnings']):
                    self._errors["text"] = ErrorList([mark_safe(
                        _("HTML validation produced %(count)d warnings. Please review the updated content below before continuing: %(messages)s") % {
                            "count": len(warnings) + len(errors),
                            "messages": '<ul><li>%s</li></ul>' % "</li><li>".join(map(escape, errors + warnings))
                        }
                    )])

                # If we're allowed to ignore warnings and we don't have any
                # errors we'll set our hidden form field to allow the user to
                # ignore warnings on the next submit:
                if not errors and settings.FEINCMS_TIDY_ALLOW_WARNINGS_OVERRIDE:
                    self.data["%s-seen_tidy_warnings" % self.prefix] = True

        return cleaned_data


class HtmlTextWidget(Widget):
    form = HtmlTextWidgetAdminForm

    #feincms_item_editor_inline = MyInline
    """
    feincms_item_editor_context_processors = (
        lambda x: settings.FEINCMS_RICHTEXT_INIT_CONTEXT,
    )
    feincms_item_editor_includes = {
        'head': ['admin/widget/htmltext/init_tinymce.html'],
    }
    """

    text = models.TextField(
        _('text'), blank=True, default="<p>%s</p>" % ('Empty element'))

    class Meta:
        abstract = True
        verbose_name = _('HTML text')
        verbose_name_plural = _('HTML texts')

    def save(self, *args, **kwargs):
        # TODO: Move this to the form?
        if getattr(self, 'cleanse', False):
            from feincms.utils.html.cleanse import cleanse_html
            self.text = cleanse_html(self.text)
        # self.rendered_content = self.render_content(kwargs)
        if self.text == '':
            self.text = "<p>%s</p>" % _('Empty element')
        super(HtmlTextWidget, self).save(*args, **kwargs)

    @classmethod
    def initialize_type(cls, cleanse=False):
        cls.cleanse = cleanse

        # TODO: Move this into somewhere more generic:
        if settings.FEINCMS_TIDY_HTML:
            # Make sure we can load the tidy function without dependency
            # failures:
            try:
                get_object(settings.FEINCMS_TIDY_FUNCTION)
            except ImportError, e:
                raise ImproperlyConfigured("FEINCMS_TIDY_HTML is enabled but the HTML tidy function %s could not be imported: %s" % (
                    settings.FEINCMS_TIDY_FUNCTION, e))
