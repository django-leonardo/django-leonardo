
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
from django.conf import settings
from django.contrib import messages
from feincms.utils import copy_model_instance

from .models import *


class PageDimensionAdmin(InlineModelAdmin):

    model = PageDimension


class PageColorSchemeInlineAdmin(admin.TabularInline):

    model = PageColorScheme

    extra = 1


def clone_branch(modeladmin, request, queryset):
    for page in queryset:
        copy = Page.objects.create(featured=page.featured,
                                   in_navigation=page.in_navigation,
                                   parent=None, theme=page.theme,
                                   color_scheme=page.color_scheme)
        copy.slug = 'copy-of-' + page.slug
        copy.title = 'Copy of ' + page.title
        copy.save()
        copy.copy_content_from(page)


def translate_branch(modeladmin, request, queryset):
    if queryset[0].parent != None or queryset.count() > 1:
        messages.error(request, "Branch must be root")
        return
    for lang in settings.LANGUAGES:
        root_page = None
        try:
            root_page = Page.objects.get(slug=lang[0])
        except:
            pass
        for page in queryset:
            if page.get_original_translation().slug != lang[0] and root_page == None:
                copy = Page.objects.create(featured=page.featured,
                                           in_navigation=page.in_navigation,
                                           parent=None, theme=page.theme,
                                           color_scheme=page.color_scheme,
                                           language=lang[0], translation_of=page)
                copy.slug = lang[0]
                copy.title = lang[1]
                copy.save()
                copy.copy_content_from(page)
                for child in page.children.all():
                    sub_copy = Page.objects.create(featured=child.featured,
                                                   in_navigation=child.in_navigation,
                                                   parent=copy, theme=child.theme,
                                                   color_scheme=child.color_scheme,
                                                   language=lang[0], translation_of=child)
                    sub_copy.slug = child.slug
                    sub_copy.title = child.title
                    sub_copy.save()
                    sub_copy.copy_content_from(child)
                    for sub_child in child.children.all():
                        sub_child_copy = Page.objects.create(featured=sub_child.featured,
                                                             in_navigation=sub_child.in_navigation,
                                                             parent=sub_copy, theme=sub_child.theme,
                                                             color_scheme=sub_child.color_scheme,
                                                             language=lang[0], translation_of=sub_child)
                        sub_child_copy.slug = sub_child.slug
                        sub_child_copy.title = sub_child.title
                        sub_child_copy.save()
                        sub_child_copy.copy_content_from(sub_child)

    messages.success(request, "Translation of branch {} was completed".format(queryset[0]))

translate_branch.short_description = "Translate branch (root page required)"


class PageAdmin(FeinPageAdmin):

    fieldsets = [
        (_('Main'), {
            'classes': ['collapse'],
            'fields': [
                'title', 'slug', 'active', 'in_navigation',
                'override_url', 'redirect_to', 'parent',
                'site', 'symlinked_page', 'language', 'translation_of'
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

    actions = [clone_branch, translate_branch]

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

            # optionally translate title and make slug
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
