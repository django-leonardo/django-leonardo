
from django import forms
from django.contrib import admin
from django.utils import translation
from django.contrib.admin.options import InlineModelAdmin, ModelAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from feincms.admin import item_editor
from feincms.module.page.modeladmins import PageAdmin as FeinPageAdmin

from .models import *


class PageDimensionAdmin(InlineModelAdmin):

    model = PageDimension


class PageColorSchemeInlineAdmin(admin.TabularInline):

    model = PageColorScheme

    extra = 1


class PageAdmin(FeinPageAdmin):

    fieldsets = [
        (None, {
            'fields': ['parent'],
        }),
        (_('Main'), {
            'classes': ['collapse'],
            'fields': [
                'title', 'slug', 'active', 'in_navigation', 'override_url', 'redirect_to', 'parent',
            ],
        }),
        (_('Styles'), {
            'classes': ['collapse'],
            'fields': [
                'template_key', 'theme', 'color_scheme', 'layout'],
        }),
        # <-- insertion point, extensions appear here, see insertion_index
        # above
        item_editor.FEINCMS_CONTENT_FIELDSET,
    ]

    def get_feincms_inlines(self, model, request):
        """ Generate genuine django inlines for registered content types. """
        model._needs_content_types()

        inlines = []
        for content_type in model._feincms_content_types:
            if not self.can_add_content(request, content_type):
                continue

            attrs = {
                '__module__': model.__module__,
                'model': content_type,
            }

            if hasattr(content_type, 'feincms_item_editor_inline'):
                inline = content_type.feincms_item_editor_inline
                attrs['form'] = inline.form

                #if hasattr(content_type, 'feincms_item_editor_form'):
                #    warnings.warn(
                #        'feincms_item_editor_form on %s is ignored because '
                #        'feincms_item_editor_inline is set too' % content_type,
                #        RuntimeWarning)

            else:
                inline = FeinCMSInline
                attrs['form'] = getattr(
                    content_type, 'feincms_item_editor_form', inline.form)

            name = '%sFeinCMSInline' % content_type.__name__
            # TODO: We generate a new class every time. Is that really wanted?
            inline_class = type(str(name), (inline,), attrs)
            inlines.append(inline_class)
        return inlines

    def get_changeform_initial_data(self, request):
        '''Copy initial data from parent'''
        initial = super(PageAdmin, self).get_changeform_initial_data(request)
        if ('translation_of' in request.GET):
            original = self.model._tree_manager.get(
                pk=request.GET.get('translation_of'))
            initial['layout'] = original.layout
            initial['theme'] = original.theme
            initial['color_scheme'] = original.color_scheme

            # optionaly translate title and make slug
            old_lang = translation.get_language()
            translation.activate(request.GET.get('language'))
            title = _(original.title)
            if title != original.title:
                initial['title'] = title
                initial['slug'] = slugify(title)
            translation.activate(old_lang)

        return initial

admin.site.register(Page, PageAdmin)


class PageDimensionAdmin(ModelAdmin):

    pass

admin.site.register(PageDimension, PageDimensionAdmin)


class WidgetDimensionAdmin(ModelAdmin):

    pass

admin.site.register(WidgetDimension, WidgetDimensionAdmin)


class WidgetDimensionInlineAdmin(GenericTabularInline):

    ct_field = "widget_type"
    ct_fk_field = "widget_id"

    model = WidgetDimension

    extra = 1


class PageColorSchemeAdmin(ModelAdmin):

    pass

admin.site.register(PageColorScheme, PageColorSchemeAdmin)


class WidgetContentThemeForm(forms.ModelForm):

    widget_class = forms.ChoiceField(
        choices=[],
        required=False,
    )

    class Meta:
        exclude = tuple()
        model = WidgetContentTheme

    def __init__(self, *args, **kwargs):
        super(WidgetContentThemeForm, self).__init__(*args, **kwargs)

        choices = [(t.model_class().__name__ if t.model_class() else None, t)
                   for t in ContentType.objects.filter(app_label__in=['web'])]
        self.fields['widget_class'].choices = choices


class WidgetContentThemeAdmin(ModelAdmin):

    form = WidgetContentThemeForm

    list_display = ('name', 'label', 'template', 'widget_class')

    list_filter = ('widget_class',)


admin.site.register(WidgetContentTheme, WidgetContentThemeAdmin)


class WidgetBaseThemeForm(forms.ModelForm):

    widget_class = forms.ChoiceField(
        choices=[],
        required=False,
    )

    class Meta:
        exclude = tuple()
        model = WidgetBaseTheme


class WidgetBaseThemeAdmin(ModelAdmin):

    form = WidgetContentThemeForm

    list_display = ('name', 'label', 'template')

admin.site.register(WidgetBaseTheme, WidgetBaseThemeAdmin)


class PageThemeAdmin(ModelAdmin):

    inlines = [PageColorSchemeInlineAdmin, ]

admin.site.register(PageTheme, PageThemeAdmin)
