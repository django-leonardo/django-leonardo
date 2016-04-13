
from __future__ import unicode_literals

import os

from django import forms
from django.conf import settings
from django.contrib.admin import widgets
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import (get_object_or_404, redirect, render,
                              render_to_response)
from django.template import RequestContext
from django.utils.encoding import uri_to_iri
from django.utils.translation import ugettext_lazy as _

from .management.commands.import_files import FileImporter
from .models import Clipboard, File, Folder, FolderRoot, Image, tools


class NewFolderForm(forms.ModelForm):

    class Meta:
        model = Folder
        fields = ('name',)
        widgets = {
            'name': widgets.AdminTextInputWidget,
        }


class ScanFolderForm(forms.Form):

    folders = forms.CharField(
        label='Path to scan', help_text='relative path from MEDIA_ROOT')

    class Meta:
        exclude = ()


def popup_status(request):
    return ('_popup' in request.GET or 'pop' in request.GET or
            '_popup' in request.POST or 'pop' in request.POST)


def selectfolder_status(request):
    return 'select_folder' in request.GET or 'select_folder' in request.POST


def popup_param(request, separator="?"):
    if popup_status(request):
        return "%s_popup=1" % separator
    else:
        return ""


def selectfolder_param(request, separator="&"):
    if selectfolder_status(request):
        return "%sselect_folder=1" % separator
    else:
        return ""


def _userperms(item, request):
    r = []
    ps = ['read', 'edit', 'add_children']
    for p in ps:
        attr = "has_%s_permission" % p
        if hasattr(item, attr):
            x = getattr(item, attr)(request)
            if x:
                r.append(p)
    return r


def canonical(request, uploaded_at, file_id):
    """
    Redirect to the current url of a public file
    """
    filer_file = get_object_or_404(File, pk=file_id, is_public=True)
    if (uploaded_at != filer_file.uploaded_at.strftime('%s') or
            not filer_file.file):
        raise Http404('No %s matches the given query.' %
                      File._meta.object_name)
    return redirect(filer_file.url)


@login_required
def edit_folder(request, folder_id):
    # TODO: implement edit_folder view
    folder = None
    return render_to_response('admin/media/folder/folder_edit.html', {
        'folder': folder,
        'is_popup': popup_status(request),
        'select_folder': selectfolder_status(request),
    }, context_instance=RequestContext(request))


@login_required
def edit_image(request, folder_id):
    # TODO: implement edit_image view
    folder = None
    return render_to_response('media/image_edit.html', {
        'folder': folder,
        'is_popup': popup_status(request),
        'select_folder': selectfolder_status(request),
    }, context_instance=RequestContext(request))


@login_required
def scan_folder(request, folder_id=None):

    if folder_id:
        folder = Folder.objects.get(id=folder_id)
    else:
        folder = None

    if request.user.is_superuser:
        pass
    elif folder is None:
        # regular users may not add root folders unless configured otherwise
        if not settings.MEDIA_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS:
            raise PermissionDenied
    elif not folder.has_add_children_permission(request):
        # the user does not have the permission to add subfolders
        raise PermissionDenied

    if request.method == 'POST':
        scan_folder_form = ScanFolderForm(request.POST)
        if scan_folder_form.is_valid():
            kwargs = {
                'path': os.path.join(settings.MEDIA_ROOT,
                                     scan_folder_form.cleaned_data['folders']),
            }
            if folder:
                kwargs['base_folder'] = folder.name
            try:
                importer = FileImporter(**kwargs)
                importer.walker(**kwargs)
            except Exception as e:
                raise e
            return render_to_response('admin/media/dismiss_popup.html',
                                      context_instance=RequestContext(request))
    else:
        new_folder_form = ScanFolderForm()
    return render_to_response('admin/media/folder/scan_form.html', {
        'new_folder_form': new_folder_form,
        'is_popup': popup_status(request),
        'select_folder': selectfolder_status(request),
    }, context_instance=RequestContext(request))


@login_required
def make_folder(request, folder_id=None):

    if not folder_id:
        folder_id = request.GET.get('parent_id')
    if not folder_id:
        folder_id = request.POST.get('parent_id')

    if folder_id:
        try:
            folder = Folder.objects.get(id=folder_id)
        except Folder.DoesNotExist:
            raise PermissionDenied
    else:
        folder = None

    if request.user.is_superuser:
        pass
    elif folder is None:
        # regular users may not add root folders unless configured otherwise
        if not settings.MEDIA_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS:
            raise PermissionDenied
    elif not folder.has_add_children_permission(request):
        # the user does not have the permission to add subfolders
        raise PermissionDenied

    if request.method == 'POST':
        new_folder_form = NewFolderForm(request.POST)
        if new_folder_form.is_valid():
            new_folder = new_folder_form.save(commit=False)
            if (folder or FolderRoot()).contains_folder(new_folder.name):
                new_folder_form._errors['name'] = new_folder_form.error_class(
                    [_('Folder with this name already exists.')])
            else:
                new_folder.parent = folder
                new_folder.owner = request.user
                new_folder.save()
                return render_to_response('admin/media/dismiss_popup.html',
                                          context_instance=RequestContext(request))
    else:
        new_folder_form = NewFolderForm()
    return render_to_response('admin/media/folder/new_folder_form.html', {
        'new_folder_form': new_folder_form,
        'is_popup': popup_status(request),
        'select_folder': selectfolder_status(request),
    }, context_instance=RequestContext(request))


class UploadFileForm(forms.ModelForm):

    class Meta:
        model = Image
        exclude = ()


@login_required
def upload(request):
    return render_to_response('media/upload.html', {
        'title': 'Upload files',
        'is_popup': popup_status(request),
        'select_folder': selectfolder_status(request),
    }, context_instance=RequestContext(request))


@login_required
def paste_clipboard_to_folder(request):
    if request.method == 'POST':
        folder = Folder.objects.get(id=request.POST.get('folder_id'))
        clipboard = Clipboard.objects.get(id=request.POST.get('clipboard_id'))
        if folder.has_add_children_permission(request):
            tools.move_files_from_clipboard_to_folder(clipboard, folder)
            tools.discard_clipboard(clipboard)
        else:
            raise PermissionDenied
    return HttpResponseRedirect('%s?order_by=-modified_at%s%s' % (
                                request.REQUEST.get('redirect_to', ''),
                                popup_param(request, separator='&'),
                                selectfolder_param(request)))


@login_required
def discard_clipboard(request):
    if request.method == 'POST':
        clipboard = Clipboard.objects.get(id=request.POST.get('clipboard_id'))
        tools.discard_clipboard(clipboard)
    return HttpResponseRedirect('%s%s%s' % (
                                request.POST.get('redirect_to', ''),
                                popup_param(request),
                                selectfolder_param(request)))


@login_required
def delete_clipboard(request):
    if request.method == 'POST':
        clipboard = Clipboard.objects.get(id=request.POST.get('clipboard_id'))
        tools.delete_clipboard(clipboard)
    return HttpResponseRedirect('%s%s%s' % (
                                request.POST.get('redirect_to', ''),
                                popup_param(request),
                                selectfolder_param(request)))


@login_required
def clone_files_from_clipboard_to_folder(request):
    if request.method == 'POST':
        clipboard = Clipboard.objects.get(id=request.POST.get('clipboard_id'))
        folder = Folder.objects.get(id=request.POST.get('folder_id'))
        tools.clone_files_from_clipboard_to_folder(clipboard, folder)
    return HttpResponseRedirect('%s%s%s' % (
                                request.POST.get('redirect_to', ''),
                                popup_param(request),
                                selectfolder_param(request)))


def directory_list(request, directory_slug, category_parent_slug):

    if directory_slug:
        directory_slug = uri_to_iri(directory_slug)

    if directory_slug is None:
        object = None
        root = getattr(settings, 'MEDIA_GALLERIES_ROOT', None)
        if root:
            obj_root = Folder.objects.get(name=root)
            object_list = Folder.objects.filter(parent=obj_root)
        else:
            object_list = Folder.objects.filter(parent=None)
    else:
        try:
            object = Folder.objects.get(id=directory_slug)
        except:
            object = Folder.objects.get(name=directory_slug)
        object_list = object.files.all()

    return render(
        request,
        'media/directory_list.html',
        {
            'object_list': object_list,
        }
    )


def directory_list_nested(request,
                          directory_slug=None,
                          parent_directory_slug=None,
                          grandparent_directory_slug=None):

    if directory_slug:
        directory_slug = uri_to_iri(directory_slug)

    if parent_directory_slug:
        parent_directory_slug = uri_to_iri(parent_directory_slug)

    if directory_slug is None:
        object = None
        root = getattr(settings, 'MEDIA_GALLERIES_ROOT', None)
        if root:
            obj_root = Folder.objects.get(name=root)
            object_list = Folder.objects.filter(parent=obj_root)
        else:
            object_list = Folder.objects.filter(parent=None)
    else:
        if parent_directory_slug is None:
            try:
                object = Folder.objects.get(id=directory_slug)
            except:
                object = Folder.objects.get(name=directory_slug)
            object_list = object.files.all()
        else:
            if grandparent_directory_slug is None:
                object = Folder.objects.get(
                    name=directory_slug, parent__name=parent_directory_slug)
                object_list = object.files.all()
            else:
                object = Folder.objects.get(
                    name=directory_slug,
                    parent__name=parent_directory_slug,
                    parent__parent__name=grandparent_directory_slug)
                object_list = object.files.all()

    return render(
        request,
        'media/directory_list_nested.html',
        {
            'object_list': object_list,
            'object': object,
        }
    )


def directory_detail_standalone(request, category_id):
    object = Folder.objects.get(id=category_id)

    return render(
        request,
        'media/directory_detail.html',
        {
            'object': object,
        },
    )
