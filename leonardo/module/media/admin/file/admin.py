
from django.contrib.admin.util import unquote
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from leonardo.forms import SelfHandlingModelForm
from leonardo.forms.fields.common import UserField
from leonardo.module.media import settings
from leonardo.module.media.fields.folder import FolderField
from leonardo.module.media.models import File
from leonardo.module.media.views import (popup_param, popup_status,
                                         selectfolder_param,
                                         selectfolder_status)

from ..permissions import PrimitivePermissionAwareModelAdmin
from .forms import FileForm


class FileAdmin(PrimitivePermissionAwareModelAdmin):
    list_display = ('label',)
    list_per_page = settings.MEDIA_PAGINATE_BY
    search_fields = ['name', 'original_filename', 'sha1', 'description']
    raw_id_fields = ('owner',)
    readonly_fields = ('sha1', 'display_canonical')

    # save_as hack, because without save_as it is impossible to hide the
    # save_and_add_another if save_as is False. To show only save_and_continue
    # and save in the submit row we need save_as=True and in
    # render_change_form() override add and change to False.
    save_as = True

    @classmethod
    def build_fieldsets(cls, extra_main_fields=(),
                        extra_advanced_fields=(), extra_fieldsets=()):
        fieldsets = (
            (None, {
                'fields': ('name', 'owner', 'file',
                           'description',) + extra_main_fields,
            }),
            (_('Advanced'), {
                'fields': ('sha1',
                           'display_canonical') + extra_advanced_fields,
                'classes': ('collapse',),
            }),
        ) + extra_fieldsets
        if settings.FILER_ENABLE_PERMISSIONS:
            fieldsets = fieldsets + (
                (None, {
                    'fields': ('is_public',)
                }),
            )
        return fieldsets

    def response_change(self, request, obj):
        """
        Overrides the default to be able to forward to the directory listing
        instead of the default change_list_view
        """
        r = super(FileAdmin, self).response_change(request, obj)
        if 'Location' in r and r['Location']:
            # it was a successful save
            if (r['Location'] in ['../'] or
                    r['Location'] == self._get_post_url(obj)):
                # this means it was a save: redirect to the directory view
                if obj.folder:
                    url = reverse('admin:filer-directory_listing',
                                  kwargs={'folder_id': obj.folder.id})
                else:
                    url = reverse(
                        'admin:filer-directory_listing-unfiled_images')
                url = "%s%s%s" % (url, popup_param(request),
                                  selectfolder_param(request, "&"))
                return HttpResponseRedirect(url)
            else:
                # this means it probably was a save_and_continue_editing
                pass
        else:
            # this means it was a save: redirect to the directory view
            if obj.folder:
                url = reverse('admin:filer-directory_listing',
                              kwargs={'folder_id': obj.folder.id})
            else:
                url = reverse(
                    'admin:filer-directory_listing-unfiled_images')
            url = "%s%s%s" % (url, popup_param(request),
                              selectfolder_param(request, "&"))
            return HttpResponseRedirect(url)

        return r

    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        extra_context = {'show_delete': True,
                         'is_popup': popup_status(request),
                         'select_folder': selectfolder_status(request), }
        context.update(extra_context)
        return super(FileAdmin, self).render_change_form(
            request=request, context=context, add=False, change=False,
            form_url=form_url, obj=obj)

    def delete_view(self, request, object_id, extra_context=None):
        """
        Overrides the default to enable redirecting to the directory view after
        deletion of a image.

        we need to fetch the object and find out who the parent is
        before super, because super will delete the object and make it
        impossible to find out the parent folder to redirect to.
        """
        parent_folder = None
        try:
            obj = self.get_queryset(request).get(pk=unquote(object_id))
            parent_folder = obj.folder
        except self.model.DoesNotExist:
            obj = None

        r = super(FileAdmin, self).delete_view(
            request=request, object_id=object_id,
            extra_context=extra_context)

        url = r.get("Location", None)

        # Check against filer_file_changelist as file deletion is always made by
        # the base class
        if (url in ["../../../../", "../../"] or
                url == reverse("admin:media_file_changelist") or
                url == reverse("admin:media_image_changelist")):
            if parent_folder:
                url = reverse('admin:filer-directory_listing',
                              kwargs={'folder_id': parent_folder.id})
            else:
                url = reverse('admin:filer-directory_listing-unfiled_images')
            url = "%s%s%s" % (url, popup_param(request),
                              selectfolder_param(request, "&"))
            return HttpResponseRedirect(url)
        return r

    def get_model_perms(self, request):
        """
        It seems this is only used for the list view. NICE :-)
        """
        return {
            'add': True,
            'change': True,
            'delete': True,
        }

    def display_canonical(self, instance):
        canonical = instance.canonical_url
        if canonical:
            return '<a href="%s">%s</a>' % (canonical, canonical)
        else:
            return '-'
    display_canonical.allow_tags = True
    display_canonical.short_description = _('canonical URL')

FileAdmin.fieldsets = FileAdmin.build_fieldsets()
