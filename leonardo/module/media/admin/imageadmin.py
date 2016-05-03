
from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext as _

from ..models import Image, ImageTranslation
from .file.admin import FileAdmin


class ImageTranslationInline(admin.StackedInline):
    model = ImageTranslation
    max_num = len(settings.LANGUAGES)


class ImageAdminForm(forms.ModelForm):
    subject_location = forms.CharField(
        max_length=64, required=False,
        label=_('Subject location'),
        help_text=_('Location of the main subject of the scene.'))

    def sidebar_image_ratio(self):
        if self.instance:
            # this is very important. It forces the value to be returned as a
            # string and always with a "." as seperator. If the conversion
            # from float to string is done in the template, the locale will
            # be used and in some cases there would be a "," instead of ".".
            # javascript would parse that to an integer.
            return '%.6F' % self.instance.sidebar_image_ratio()
        else:
            return ''

    class Meta:
        model = Image
        exclude = ()

    class Media:
        css = {}
        js = ()


class ImageAdmin(FileAdmin):
    form = ImageAdminForm
    inlines = [ImageTranslationInline]

ImageAdmin.fieldsets = ImageAdmin.build_fieldsets(
    extra_main_fields=('author', 'default_alt_text', 'default_caption',),
    extra_fieldsets=(
        ('Subject Location', {
            'fields': ('subject_location',),
            'classes': ('collapse',),
        }),
    )
)
