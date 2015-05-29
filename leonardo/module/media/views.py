
from __future__ import unicode_literals

import os

from django import forms
from django.conf import settings
from django.contrib.admin import widgets
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from . import settings as filer_settings

from .management.commands.import_files import FileImporter
from .models import Folder, Clipboard, FolderRoot, Image, tools
from feincms.views.decorators import standalone


class NewFolderForm(forms.ModelForm):

    class Meta:
        model = Folder
        fields = ('name',)
        widgets = {
            'name': widgets.AdminTextInputWidget,
        }


class ScanFolderForm(forms.Form):

    path = forms.CharField(
        label='Path to scan', help_text='relative path to MEDIA_ROOT')

    class Meta:
        exclude = ()


def popup_status(request):
    return '_popup' in request.REQUEST or 'pop' in request.REQUEST


def selectfolder_status(request):
    return 'select_folder' in request.REQUEST


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
        if not filer_settings.FILER_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS:
            raise PermissionDenied
    elif not folder.has_add_children_permission(request):
        # the user does not have the permission to add subfolders
        raise PermissionDenied

    if request.method == 'POST':
        scan_folder_form = ScanFolderForm(request.POST)
        if scan_folder_form.is_valid():
            kwargs = {
                'path': os.path.join(settings.MEDIA_ROOT,
                                     scan_folder_form.cleaned_data['path']),
            }
            if folder:
                kwargs['base_folder'] = folder.name
            try:
                importer = FileImporter(**kwargs)
                importer.walker(**kwargs)
            except Exception, e:
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
        folder_id = request.REQUEST.get('parent_id', None)
    if folder_id:
        folder = Folder.objects.get(id=folder_id)
    else:
        folder = None

    if request.user.is_superuser:
        pass
    elif folder is None:
        # regular users may not add root folders unless configured otherwise
        if not filer_settings.FILER_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS:
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


def category_list(request, category_slug, category_parent_slug):
    if category_slug is None:
        category_list = Folder.objects.filter(mptt_level=0)
        category = None
    else:
        category = Folder.objects.get(name=category_slug)
        category_list = Folder.objects.filter(parent=category)
    return render_to_response(
        'media/category_list.html', {
            'object_list': category_list,
            'object': category,
        },
        context_instance=RequestContext(request)
    )


#@standalone
def category_list_nested(request,
                         category_slug=None,
                         parent_category_slug=None,
                         grandparent_category_slug=None):
    if category_slug is None:
        object = None
        object_list = Folder.objects.filter(parent=None)
    else:
        if parent_category_slug is None:
            object = Folder.objects.get(id=category_slug)
            object_list = object.children.all()
        else:
            if grandparent_category_slug is None:
                object = Folder.objects.get(
                    name=category_slug, parent__name=parent_category_slug)
                object_list = object.children.all()
            else:
                object = Folder.objects.get(
                    name=category_slug,
                    parent__name=parent_category_slug,
                    parent__parent__name=grandparent_category_slug)
                object_list = object.children.all()

    return render_to_response(
        'media/category_list_nested.html', {
            'object_list': object_list,
            'object': object,
        },
        context_instance=RequestContext(request, {'standalone': True})
    )


@standalone
def category_detail_standalone(request, category_id):
    object = Folder.objects.get(id=category_id)

    return render_to_response(
        'media/category_detail_standalone.html', {
            'object': object,
        },
        context_instance=RequestContext(request)
    )
