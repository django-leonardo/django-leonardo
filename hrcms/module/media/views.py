# -*- coding: UTF-8 -*-

import os
import glob

from django import forms

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, RequestContext, loader
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _, ugettext as __
from django.utils.encoding import smart_str
from django.views.generic.simple import direct_to_template
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

from django.template.defaultfilters import slugify

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from feincms.views.decorators import standalone

from webcms.module.media.models import File, FileTranslation, Category

def category_xml_detail(request, object_id):
    obj = Category.objects.get(pk=object_id)

    data = render_to_string('media/category_detail.xml', {
        'object': obj,
        'request': request,
    })

    response = HttpResponse(data, mimetype='text/xml')
    return response

def category_list(request, category_slug, category_parent_slug):
    if category_slug == None:
        category_list = Category.objects.filter(active=True, mptt_level=0).order_by('sort_order')
        category = None
    else:
        category = Category.objects.get(name=category_slug)
        category_list = Category.objects.filter(active=True, parent=category).order_by('sort_order')
    return render_to_response(
        'media/category_list.html', {
            'object_list': category_list,
            'object': category,
        },
        context_instance=RequestContext(request)
    )

def category_list_nested(request, category_slug=None, parent_category_slug=None, grandparent_category_slug=None):
    if category_slug == None:
        object = None
        object_list = Category.objects.filter(active=True, mptt_level=0)
    else:
        if parent_category_slug == None:
            object = Category.objects.get(name=category_slug)
            object_list = object.children.all()
        else:
            if grandparent_category_slug == None:
                object = Category.objects.get(name=category_slug, parent__name=parent_category_slug)
                object_list = object.children.all()
            else:
                object = Category.objects.get(name=category_slug, parent__name=parent_category_slug, parent__parent__name=grandparent_category_slug)
                object_list = object.children.all()

    return render_to_response(
        'media/category_list_nested.html', {
            'object_list': object_list,
            'object': object,
        },
        context_instance=RequestContext(request)
    )

@standalone
def category_detail_standalone(request, category_id):
    object = Category.objects.get(id=category_id)

    return render_to_response(
        'media/category_detail_standalone.html', {
            'object': object,
        },
        context_instance=RequestContext(request)
    )

class MediaScanForm(forms.Form):
    pass

@staff_member_required
def scan_files(request):
    report = False
    if request.method == 'POST':
        form = MediaScanForm(request.POST)
        data1 = glob.glob('%s/files/*' % settings.MEDIA_ROOT)
        data2 = glob.glob('%s/files/*/*' % settings.MEDIA_ROOT)
        data3 = glob.glob('%s/files/*/*/*' % settings.MEDIA_ROOT)
        data4 = glob.glob('%s/files/*/*/*/*' % settings.MEDIA_ROOT)
        data = data1 + data2 + data3 + data4
        parsed_data = []
        for raw_file in data:
            if os.path.isdir(raw_file):
                file = raw_file.replace('%s/files/' % settings.MEDIA_ROOT, '')
                is_new = False
                if file.count('/') == 0:
                    try:
                        ffile = File.objects.get(name=file)
                    except:
                        ffile = File(name=file)
                        ffile.save()
                        is_new = True
                if file.count('/') == 1:
                    file_parts = file.split('/')
                    parent = File.objects.get(name=file_parts[0])
                    try:
                        ffile = File.objects.get(folder__name=file_parts[0], name=file_parts[1])
                    except:
                        ffile = File(name=file_parts[1])
                        ffile.folder = parent
                        ffile.save()
                        is_new = True
                if file.count('/') == 2:
                    file_parts = file.split('/')
                    parent = File.objects.get(folder__name=file_parts[0], name=file_parts[1])
                    try:
                        ffile = File.objects.get(folder__folder__name=file_parts[0], folder__name=file_parts[1], name=file_parts[2])
                    except:
                        ffile = File(name=file_parts[2])
                        ffile.folder = parent
                        ffile.save()
                        is_new = True
                if file.count('/') == 3:
                    file_parts = file.split('/')
                    parent = File.objects.get(folder__folder__name=file_parts[0], folder__name=file_parts[1], name=file_parts[2])
                    try:
                        ffile = File.objects.get(folder__folder__folder__name=file_parts[0], folder__folder__name=file_parts[1], folder__name=file_parts[2], name=file_parts[3])
                    except:
                        ffile = File(name=file_parts[3])
                        ffile.folder = parent
                        ffile.save()
                        is_new = True
                if file.count('/') == 4:
                    file_parts = file.split('/')
                    parent = File.objects.get(folder__folder__folder__name=file_parts[0], folder__folder__name=file_parts[1], folder__name=file_parts[2], name=file_parts[3])
                    try:
                        ffile = File.objects.get(folder__folder__folder__folder__name=file_parts[0], folder__folder__folder__name=file_parts[1], folder__folder__name=file_parts[2], folder__name=file_parts[3], name=file_parts[4])
                    except:
                        ffile = File(name=file_parts[4])
                        ffile.folder = parent
                        ffile.save()
                        is_new = True
                parsed_data.append({
                    'file': file,
                    'is_new': is_new,
                })
        for raw_file in data:
            if os.path.isfile(raw_file):
                file = raw_file.replace('%s/files/' % settings.MEDIA_ROOT, '')
                is_new = False
                file_parts = file.split('/')
                folder = None
                if file.count('/') == 1:
                    folder = File.objects.get(name=file_parts[0])
                if file.count('/') == 2:
                    folder = File.objects.get(folder__name=file_parts[0], name=file_parts[1])
                if file.count('/') == 3:
                    folder = File.objects.get(folder__folder__name=file_parts[0], folder__name=file_parts[1], name=file_parts[2])
                try:
                    ffile = File.objects.get(file=file)
                except:
                    ffile = File(file=file)
                    ffile.folder = folder
                    ffile.save()
                    is_new = True

                parsed_data.append({
                    'file': file,
                    'is_new': is_new,
                })
        report = render_to_string('admin/media/scan_report.html', {
            'data': parsed_data,
        })
    else:
        form = MediaScanForm()
    return direct_to_template(request,
        template = 'admin/media/scan_files.html',
        extra_context = {
            'form': form,
            'report': report
        }
    )

class CreateFolderForm(forms.Form):
    name = forms.CharField(max_length=60, label=_("Folder name"), required=True)
    folder = forms.ChoiceField(label=_("Location"), help_text=("Where to create a new folder."), required=False)

    def __init__(self, *args, **kwargs):
        super(CreateFolderForm, self).__init__(*args, **kwargs)

        choices = []
        choices.append(('', '------------'))
        root_medias = File.objects.filter(folder=None, type='folder')
        for root_media in root_medias:
            choices.append((root_media.id, root_media.__unicode__(),))
            for sub_root_media in root_media.parent.filter(type='folder'):
                choices.append((sub_root_media.id, u'—%s' % sub_root_media.__unicode__(),))
                for sub_sub_root_media in sub_root_media.parent.filter(type='folder'):
                    choices.append((sub_sub_root_media.id, u'——%s' % sub_sub_root_media.__unicode__(),))
                    for sub_sub_sub_root_media in sub_sub_root_media.parent.filter(type='folder'):
                        choices.append((sub_sub_sub_root_media.id, u'———%s' % sub_sub_sub_root_media.__unicode__(),))

        self.fields['folder'].choices = choices

    def clean(self):
        cleaned_data = super(CreateFolderForm, self).clean()
        folder_id = cleaned_data.get("folder", False)
        name = cleaned_data.get("name")
        slug = slugify(name)
        if folder_id:
            folder = File.objects.get(pk=folder_id)
            path = os.path.join(settings.WEBCMS_MEDIA_ROOT, folder.path(), folder.name, slug)
        else:
            path = os.path.join(settings.WEBCMS_MEDIA_ROOT, slug)
        if os.path.isdir(path):
            raise forms.ValidationError("Folder with this name already exists.")
        if os.path.exists(path):
            raise forms.ValidationError("File or link with this name already exists.")

        # Always return the full collection of cleaned data.
        return cleaned_data

@staff_member_required
def select_folder(request):
    choices = []
    root_medias = File.objects.filter(folder=None, type='folder')
    for root_media in root_medias:
        choices.append((root_media.id, root_media.__unicode__(),))
        for sub_root_media in root_media.parent.filter(type='folder'):
            choices.append((sub_root_media.id, u'—%s' % sub_root_media.__unicode__(),))
            for sub_sub_root_media in sub_root_media.parent.filter(type='folder'):
                choices.append((sub_sub_root_media.id, u'——%s' % sub_sub_root_media.__unicode__(),))
                for sub_sub_sub_root_media in sub_sub_root_media.parent.filter(type='folder'):
                    choices.append((sub_sub_sub_root_media.id, u'———%s' % sub_sub_sub_root_media.__unicode__(),))

    return direct_to_template(request,
        template = 'admin/media/select_folder.html',
        extra_context = {
            'choices': choices,
        }
    )

@staff_member_required
def create_folder(request):
    if request.method == 'POST':
        form = CreateFolderForm(request.POST)
        if form.is_valid():
            name = slugify(form.cleaned_data.get('name'))
            if form.cleaned_data.get('folder', False):
                folder = File.objects.get(pk=form.cleaned_data.get('folder'))
            file_kwargs = {
                'name': name
            }
            file_translation_kwargs = {
                'name': form.cleaned_data.get('name')
            }
            if form.cleaned_data.get('folder', False):
                file_kwargs['folder'] = folder
            new_file = File(**file_kwargs)
            new_file.save()
            file_translation_kwargs['parent'] = new_file
            new_file_translation = FileTranslation(**file_translation_kwargs)
            new_file_translation.save()
            return HttpResponseRedirect('/admin/media/file/?type__exact=folder')
    else:
        form = CreateFolderForm()
    return direct_to_template(request,
        template = 'admin/media/create_folder.html',
        extra_context = {
            'form': form,
        }
    )

class UploadFileForm(forms.ModelForm):
#    file = forms.FileField()

    class Meta:
        model = File
        fields = ('file',)

def _upload_file(request, folder, form):
    mediafile = form.save(commit=False)
    mediafile.folder = folder
    mediafile.save()
    strip_path = mediafile.file.name.split('/')
    caption = strip_path[-1]
    caption = caption.replace("_", " ")
    caption = caption.strip()
    translation = FileTranslation(**{
        'name': caption,
        'language_code': request.LANGUAGE_CODE,
        'parent': mediafile
    })
    translation.save()
    return mediafile

@never_cache
@staff_member_required
def upload_files(request, folder_id):
    async = request.POST.get('async', 'no')
    folder = File.objects.get(pk=folder_id)
    file = False
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = _upload_file(request, folder, form)
        if async == 'no':
            return HttpResponseRedirect('.')
    else:
        form = UploadFileForm()
    return direct_to_template(request,
        template = 'admin/media/upload_files.html',
        extra_context = {
            'form': form,
            'folder': folder,
            'async': async,
            'file': file
        }
    )

@standalone
@csrf_exempt
def upload_files_process(request, folder_id):
    folder = File.objects.get(pk=folder_id)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file = _upload_file(request, folder, form)
        return HttpResponse('OK')