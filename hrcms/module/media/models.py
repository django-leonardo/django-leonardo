# -*- coding: utf-8 -*-

import shutil

import re
import os
import logging
from PIL import Image

from datetime import datetime

from django.conf.urls.defaults import url, patterns

from django.contrib import admin, messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.template.defaultfilters import filesizeformat
from django.utils.safestring import mark_safe
from django.utils import translation
from django.utils.translation import ugettext_lazy as _, ugettext as __
from django.template.defaultfilters import slugify
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect

from django.core.files.base import ContentFile
from django.core.cache import cache

from feincms.models import Base

from feincms.templatetags import feincms_thumbnail
from feincms.translations import TranslatedObjectMixin, Translation, TranslatedObjectManager
from feincms.module.page.extensions.navigation import NavigationExtension, PagePretender
from feincms.content.application.models import reverse

from mptt.models import MPTTModel
from mptt.admin import MPTTModelAdmin

from sorl.thumbnail import get_thumbnail

from tinymce.models import HTMLField
from webcms.utils.models import JSONField

log = logging.getLogger('webcms_module.media')

from livesettings import config_value

from webcms.module.media.config import MEDIA_GROUP
#default_storage_class = getattr(settings, 'DEFAULT_FILE_STORAGE', 'django.core.files.storage.FileSystemStorage')
#default_storage = get_callable(default_storage_class)
#file_storage = default_storage(location=settings.WEBCMS_MEDIA_ROOT, base_url=settings.WEBCMS_MEDIA_URL)

from django.core.files.storage import FileSystemStorage

class OverwriteStorage(FileSystemStorage):
    """
    Returns same name for existing file and deletes existing file on save.
    """
    def _save(self, name, content):
        if self.exists(name.encode('utf-8')):
            self.delete(name.encode('utf-8'))
        return super(OverwriteStorage, self)._save(name, content)

    def get_available_name(self, name):
        return name

file_storage = OverwriteStorage(location=settings.WEBCMS_MEDIA_ROOT, base_url=settings.WEBCMS_MEDIA_URL)

def get_file_path(instance, filename):
    path =instance.path()
    return os.path.join(path.encode('utf-8'), filename.encode('utf-8'))

class Category(MPTTModel, TranslatedObjectMixin):
    """
    An encapsulation of a media category.
    """
    name = models.SlugField(max_length=127, verbose_name=_('name'), help_text=_("URL friendly name of the media category."))
    sort_order = models.IntegerField(default=0, verbose_name=_('sort order'))
    created = models.DateTimeField(_('created'), default=datetime.now)
    active = models.BooleanField(default=True, verbose_name=_('is active?'))
    hidden = models.BooleanField(default=False, verbose_name=_('is hidden?'))
    sync_with = models.ForeignKey('File', verbose_name=_('sync'), blank=True, null=True, related_name='sync_with', limit_choices_to= {'type': 'folder' })
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    objects = TranslatedObjectManager()

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        if self.sync_with:
            files = File.objects.filter(folder=self.sync_with).exclude(type='folder')
            ids = []
            creates = {}
            for file in files:
                ids.append(file.id)
                creates[file.id] = file
            log.debug(files)
            log.debug(self.media.all())
            for catfile in self.media.all():
                if catfile.file.id in ids:
                    creates.pop(catfile.file.id)
            log.debug(creates)
            for key, create in creates.items():
                catfile = CategoryFile(file=create, category=self)
                catfile.save()
        self.purge_translation_cache()

    class Meta:
        verbose_name = _('media category')
        verbose_name_plural = _('media categories')
        ordering=['sort_order']

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['sort_order']

    def get_featured_image(self):
        """
        Gets first featured image or first image in gallery
        """
        try:
            cat_file = CategoryFile.objects.filter(category=self, file__type='image', featured=True, active=True)[0]
        except:
            try:
                cat_file = CategoryFile.objects.filter(category=self, file__type='image', active=True)[0]
            except:
                return None
        return cat_file.file

    def __unicode__(self):
       # return self.name
        trans = None
#        trans = cache.get('media_cat_%s' % self.id)
        if trans != None:
            log.debug('cat has translation!')
            return trans   
        if hasattr(self, "preferred_translation"):
            trans = getattr(self, "preferred_translation", u"")
            logging.debug('cat has trans!!!!!')
        else:
            try:
                trans = unicode(self.translation)
            except models.ObjectDoesNotExist:
                pass
            except AttributeError, e:
                pass

        if trans == None:
            trans = self.name
#        cache.set('media_cat_%s' % self.id, trans, 720000)
#        if self.parent:
#            trans = '%s / %s' % (self.parent.__unicode__(), trans)
        return trans

    def title(self):
        trans = self.__unicode__()
        if self.parent:
            trans = '%s / %s' % (self.parent.__unicode__(), trans)
        return trans


class CategoryTranslation(Translation(Category)):
    """
    Translations for category.
    """
    name = models.CharField(max_length=255, verbose_name=_("name"))
    excerpt = HTMLField(_('excerpt'), blank=True, null=True)
    description = HTMLField(_('description'), blank=True, null=True)

    class Meta:
        verbose_name = _('category translation')
        verbose_name_plural = _('category translations')

    def __unicode__(self):
        return self.name

class MediaCategoryNavigationExtension(NavigationExtension):
    name = _('all media categories')

    def children(self, page, **kwargs):
        for category in Category.objects.filter(active=True):
            yield PagePretender(
                title=category.__unicode__(),
                url= '/'#reverse('project.eas_product.apps.product_list/category_detail', kwargs={'category_slug': category.slug}),
            )

class FileBase(Base, TranslatedObjectMixin):
    """
    Abstract media file class. Inherits from :class:`feincms.module.Base`
    because of the (handy) extension mechanism.
    """

    file = models.FileField(_('file'), max_length=255, upload_to=get_file_path, storage=file_storage, blank=True)
    name = models.CharField(_('file name'), max_length=255, blank=True)
    type = models.CharField(_('file type'), max_length=12, editable=False, choices=())
    created = models.DateTimeField(_('created'), editable=False, default=datetime.now)
    copyright = models.CharField(_('copyright'), max_length=200, blank=True)
    size  = models.IntegerField(_("file size"), blank=True, null=True, editable=False)
    hash = models.CharField(_('hash'), max_length=200, blank=True)
    meta = JSONField(_('metadata'), blank=True, editable=False)
    folder = models.ForeignKey('self', related_name='parent', verbose_name=_('folder'), blank=True, null=True, limit_choices_to= {'type': 'folder' })
    categories = models.ManyToManyField(Category, verbose_name=_('categories'), blank=True, null=True, through='CategoryFile')
    categories.category_filter = True

    class Meta:
        abstract = True
        verbose_name = _('media file')
        verbose_name_plural = _('media files')

    objects = TranslatedObjectManager()

    filetypes = [ ]
    filetypes_dict = { }

    def path_fragment(self):
        if self.file:
            return self.file.name
        else:
            return self.name

    def path(self):
        path_list = []
        if self.folder:
            if self.folder.folder:
                path_list.append(self.folder.folder.name)
                if self.folder.folder.folder:
                    path_list.append(self.folder.folder.folder.name)
            path_list.append(self.folder.name)
#        path_list.append(self.name)
        if len(path_list) > 0:
            return os.path.join(*path_list)
        else:
            return ''
    path.short_description = _("full path")
    path.admin_order_field = 'full_path'

    def formatted_size(self):
        return filesizeformat(self.size)
    formatted_size.short_description = _("file size")
    formatted_size.admin_order_field = 'file_size'

    def formatted_created(self):
        return self.created.strftime("%Y-%m-%d %H:%M")
    formatted_created.short_description = _("created")
    formatted_created.admin_order_field = 'created'

    @classmethod
    def reconfigure(cls, upload_to=None, storage=None):
        f = cls._meta.get_field('file')
        # Ugh. Copied relevant parts from django/db/models/fields/files.py
        # FileField.__init__ (around line 225)
        if storage:
            f.storage = storage
        if upload_to:
            f.upload_to = upload_to
            if callable(upload_to):
                f.generate_filename = upload_to

    @classmethod
    def register_filetypes(cls, *types):
        cls.filetypes[0:0] = types
        choices = [ t[0:2] for t in cls.filetypes ]
        cls.filetypes_dict = dict(choices)
        cls._meta.get_field('type').choices[:] = choices

    def __init__(self, *args, **kwargs):
        super(FileBase, self).__init__(*args, **kwargs)
        if self.file and self.file.path:
            self._original_file_path = self.file.path

    def __unicode__(self):
        trans = cache.get('media_file_%s' % self.id)
        if trans == None or trans == "":
            if self.file:
                trans = self.file.name
            else:
                trans = self.name
            cache.set('media_file_%s' % self.id, trans, 1000000)
            log.debug('media does not have translation! id: %s' % self.id)
        return trans
        trans = None
        trans = cache.get('media_file_%s' % self.id)
        if trans != None:
            trans = unicode(trans)
            if trans.strip():
                log.debug('has translation!')
                return trans
        try:
            trans = self.translation
        except models.ObjectDoesNotExist:
            pass
        except AttributeError:
            pass

        if trans:
            trans = unicode(trans)
            if trans.strip():
                log.debug('does not have translation! id: %s' % self.id)
                cache.set('media_file_%s' % self.id, trans, 1000000)
                return trans
        trans = os.path.basename(self.file.name)
        cache.set('media_file_%s' % self.id, trans, 1000000)
        return trans
    """
    def __unicode__(self):
        trans = None

        # This might be provided using a .extra() clause to avoid hundreds of extra queries:
        if hasattr(self, "preferred_translation"):
            log.debug('has translation!')
            trans = getattr(self, "preferred_translation", u"")
        else:
            pass
#            try:
#                trans = cache.get('file_title_%s' % self.id)
#            else:
#                try:
#                    trans = unicode(self.translation)
#                except models.ObjectDoesNotExist:
#                    pass
#                except AttributeError, e:
#                    pass
            except:
                pass

        if trans:
            return trans
        else:
            if self.folder != None:
                if self.folder.folder != None:
                    if self.folder.folder.folder != None:
                        if self.folder.folder.folder.folder != None:
                            name = '%s %s %s %s %s' % (self.folder.folder.folder.folder.name, self.folder.folder.folder.name, self.folder.folder.name, self.folder.name, self.name)
                        else:
                            name = '%s %s %s %s' % (self.folder.folder.folder.name, self.folder.folder.name, self.folder.name, self.name)
                    else:
                        name = '%s %s %s' % (self.folder.folder.name, self.folder.name, self.name)
                else:
                    name = '%s %s' % (self.folder.name, self.name)
            else:
                name = self.name
            translation = FileTranslation(name=name, parent=self, language_code=settings.LANGUAGE_CODE)
            translation.save()
            trans = cache.set('file_title_%s_%s' % (settings.LANGUAGE_CODE, self.id), translation.name, 24000)
            return name
    """

    def get_absolute_url(self):
        return self.file.url

    def file_type(self):
        t = self.filetypes_dict[self.type]
        if self.type == 'image':
            try:
                from django.core.files.images import get_image_dimensions
                d = get_image_dimensions(self.file.file)
                if d: t += "<br/>%d&times;%d" % ( d[0], d[1] )
            except IOError, e:
                t += "<br/>(%s)" % e.strerror
        return t
    file_type.admin_order_field = 'type'
    file_type.short_description = _('file type')
    file_type.allow_tags = True

    def file_info(self):
        """
        Method for showing the file name in admin.

        Note: This also includes a hidden field that can be used to extract
        the file name later on, this can be used to access the file name from
        JS, like for example a TinyMCE connector shim.
        """
        from os.path import basename
        from feincms.utils import shorten_string
        return u'<input type="hidden" class="medialibrary_file_path" name="_media_path_%d" value="%s" /> %s' % (
                self.id,
                self.file.name,
                shorten_string(basename(self.file.name), max_length=28), )
    file_info.short_description = _('file info')
    file_info.allow_tags = True

    def determine_file_type(self, name):
        """
        >>> t = MediaFileBase()
        >>> t.determine_file_type('foobar.jpg')
        'image'
        >>> t.determine_file_type('foobar.PDF')
        'pdf'
        >>> t.determine_file_type('foobar.jpg.pdf')
        'pdf'
        >>> t.determine_file_type('foobar.jgp')
        'other'
        >>> t.determine_file_type('foobar-jpg')
        'other'
        """
        for type_key, type_name, type_test in self.filetypes:
            if type_test(name):
                return type_key
        return self.filetypes[-1][0]

    def save(self, *args, **kwargs):
        if not self.id and not self.created:
            self.created = datetime.now()
        if self.file:
            self.name = os.path.basename(self.file.name)

            self.type = self.determine_file_type(self.file.name)
            if self.file:
                try:
                    self.size = self.file.size
                except (OSError, IOError, ValueError), e:
                    logging.error("Unable to read file size for %s: %s", self, e)

            # Try to detect things that are not really images
            if self.type == 'image':
                try:
                    try:
                        image = Image.open(self.file)
                    except (OSError, IOError):
                        image = Image.open(self.file.path)

                    # Rotate image based on exif data.

                    """
                    if image:
                        try:
                            exif = image._getexif()
                        except (AttributeError, IOError):
                            exif = False
                        # PIL < 1.1.7 chokes on JPEGs with minimal EXIF data and
                        # throws a KeyError deep in its guts.
                        except KeyError:
                            exif = False

                        if exif:
                            orientation = exif.get(274)
                            rotation = 0
                            if orientation == 3:
                                rotation = 180
                            elif orientation == 6:
                                rotation = 270
                            elif orientation == 8:
                                rotation = 90
                            if rotation:
                                image = image.rotate(rotation)
                                image.save(self.file.path)
                    """
                except (OSError, IOError), e:
                    self.type = self.determine_file_type('***') # It's binary something

            if getattr(self, '_original_file_path', None):
                if self.file.path != self._original_file_path:
                    try:
                        os.unlink(self._original_file_path)
                    except:
                        pass
        else:
            self.type = 'folder'
        super(FileBase, self).save(*args, **kwargs)
        sync_categories = config_value('MEDIA','SYNC_FOLDERS', False)
        if self.type == 'folder' and sync_categories:
            categories = Category.objects.filter(sync_with=self)
            if categories.count() == 0:
                category = Category(name=self.name, sync_with=self)
                if self.folder:
                    parent_categories = Category.objects.filter(sync_with=self.folder)
                    if parent_categories.count() > 0:
                        category.parent = parent_categories[0]
                category.save()
        if self.type != 'folder' and sync_categories:
            if self.folder:
                parent_categories = Category.objects.filter(sync_with=self.folder)
                if parent_categories.count() > 0:
                    parent_categories[0].save()
        if self.type == 'folder':
            path = os.path.join(settings.WEBCMS_MEDIA_ROOT, self.path(), self.name)
            if not os.path.exists(path):
                os.makedirs(path)

        cache.set('media_file_%s' % self.id, self.name, -1)
        name = self.__unicode__()
        #self.purge_translation_cache()

    def delete(self, *args, **kwargs):
        if self.type == 'folder':
            path = os.path.join(settings.WEBCMS_MEDIA_ROOT, self.path(), self.name)
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except:
                pass
        else:
            try:
                path = os.path.join(self.file.name)
                os.remove(path)
            except:
                pass

        super(FileBase, self).delete(*args, **kwargs)

FileBase.register_filetypes(
        # Should we be using imghdr.what instead of extension guessing?
        ('image', _('Image'), lambda f: re.compile(r'\.(bmp|jpe?g|jp2|jxr|gif|png|tiff?)$', re.IGNORECASE).search(f)),
        ('video', _('Video'), lambda f: re.compile(r'\.(mov|m[14]v|mp4|avi|mpe?g|qt|ogv|wmv)$', re.IGNORECASE).search(f)),
        ('audio', _('Audio'), lambda f: re.compile(r'\.(au|mp3|m4a|wma|oga|ram|wav)$', re.IGNORECASE).search(f)),
        ('graph', _('Graph'), lambda f: re.compile(r'\.(graphml|graphmlz)$', re.IGNORECASE).search(f)),
        ('owl', _('Ontology'), lambda f: f.lower().endswith('.owl')),
        ('pdf', _('PDF document'), lambda f: f.lower().endswith('.pdf')),
        ('swf', _('Flash'), lambda f: f.lower().endswith('.swf')),
        ('txt', _('Text'), lambda f: f.lower().endswith('.txt')),
        ('rtf', _('Rich text'), lambda f: f.lower().endswith('.rtf')),
        ('svg', _('Vector graphics'), lambda f: f.lower().endswith('.svg')),
        ('zip', _('Zip archive'), lambda f: f.lower().endswith('.zip')),
        ('doc', _('Microsoft Word'), lambda f: re.compile(r'\.docx?$', re.IGNORECASE).search(f)),
        ('xls', _('Microsoft Excel'), lambda f: re.compile(r'\.xlsx?$', re.IGNORECASE).search(f)),
        ('ppt', _('Microsoft PowerPoint'), lambda f: re.compile(r'\.pptx?$', re.IGNORECASE).search(f)),
        ('other', _('Binary'), lambda f: True), # Must be last
        ('folder', _('Folder'), lambda f: True),
    )

class File(FileBase):
    @classmethod
    def register_extension(cls, register_fn):
        register_fn(cls, FileAdmin)

class FileTranslation(Translation(File)):
    """
    Translated media file name and description.
    """

    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('media file translation')
        verbose_name_plural = _('media file translations')

    def __unicode__(self):
        return self.name

class FileTranslation_Inline(admin.StackedInline):
    model   = FileTranslation
    max_num = len(settings.LANGUAGES)

def admin_thumbnail(obj):
    if obj.type == 'image':
        image = None
        try:
            image = get_thumbnail(obj.file, '100x100', crop='center', format='PNG')
        except:
            pass

        if image:
            return mark_safe(u"""
                <a href="%(url)s" target="_blank">
                    <img src="%(image)s" alt="" />
                </a>""" % {
                    'url': obj.file.url,
                    'image': image.url,})
    return ''
admin_thumbnail.short_description = _('Preview')
admin_thumbnail.allow_tags = True

class CategoryFile(models.Model):
    category = models.ForeignKey(Category, related_name='media', verbose_name=_('category'))
    file = models.ForeignKey(File, verbose_name=_('file'))
    sort_order = models.IntegerField(verbose_name=_('ordering'), default=0)
    featured = models.BooleanField(verbose_name=_('featured'), default=False)
    active = models.BooleanField(verbose_name=_('active'), default=True)

    class Meta:
        ordering = ['sort_order', ]
        verbose_name = _('category file')
        verbose_name_plural = _('category files')


class MediaCategoriesNavigationExtension(NavigationExtension):
    name = _('All media categories')

    def children(self, page, **kwargs):
        result = []
        base_url = page.get_absolute_url()
        category_list = Category.objects.filter(active=True, parent=None).order_by('sort_order')
        for category in category_list:
            subchildren = []
            for subcategory in category.get_children():
                if subcategory.active:
                    subchildren.append(PagePretender(
                        title=subcategory.__unicode__(),
                        url= '%s%s/%s/' % (base_url, category.name, subcategory.name),
                    ))
            page_pretender = PagePretender(
                title=category.__unicode__(),
                url= '%s%s/' % (base_url, category.name),
                children = subchildren
            )
            result.append(page_pretender)
        return result

class CategoryFile_Inline(admin.TabularInline):
    model = CategoryFile
    extra = 5

class CategoryTranslation_Inline(admin.StackedInline):
    model = CategoryTranslation
    extra = 5

class CategoryAdmin(MPTTModelAdmin):
    list_display = ['__unicode__', 'active', 'sort_order', 'sync_with']
    list_editable = ['active',]
    list_filter = ['active']
    list_per_page = 25
    inlines = [CategoryTranslation_Inline,]# CategoryFile_Inline] 

def file_actions(obj):
    if obj.type == 'folder':
        url = "<a href='/webcms-media/upload-files/%s/'>%s</a>" % (obj.id, __("Upload files"))
        return url
    else:
        return ''
file_actions.short_description = _('Actions')
file_actions.allow_tags = True

class FileAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    inlines = [FileTranslation_Inline, CategoryFile_Inline]
    list_display = ['__unicode__', admin_thumbnail, 'file_type', 'path', 'name', 'formatted_size', 'formatted_created', file_actions]
    list_filter = ['type', 'categories']
    list_per_page = 25
    search_fields  = ['copyright', 'file', 'translations__name']
    filter_horizontal = ("categories",)

    def get_urls(self):

        urls = super(FileAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^file-bulk-upload/$', self.admin_site.admin_view(FileAdmin.bulk_upload), {}, name='file_bulk_upload'),
#            url(r'^file-flash-upload/$', self.admin_site.admin_view(FileAdmin.bulk_upload), {}, name='file_bulk_upload'),
            url(r'^flash-upload-process/$', self.admin_site.admin_view(FileAdmin.flash_upload), {}, name='file_upload_process'),
        )

        return my_urls + urls

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['folders'] = File.objects.filter(type='folder')
        return super(FileAdmin, self).changelist_view(request, extra_context=extra_context)

    @staticmethod
    @csrf_protect
#    @permission_required('media.add_file')
    def flash_upload(request):
        from django.core.urlresolvers import reverse
        from django.utils.functional import lazy

        def import_file(request, folder_id, file):

            file_name = file.name

            name, ext = os.path.splitext(file_name)

            new_file = File()
            new_file.name = file_name
            target_filename = new_file.name

            if folder_id:
                folder = File.objects.get(pk=int(folder_id))
                new_file.folder = folder
#                target_filename = os.path.join(new_file.path(), new_file.name)

            new_file.file.save(target_filename, ContentFile(file.read()))
            new_file.save()

        if request.method == 'POST' and 'file' in request.FILES:
            import_file(request, request.POST.get('folder'), request.FILES['file'])
        else:
            messages.error(request, _("No input file given"))

        return HttpResponseRedirect(reverse('webcms_admin:media_file_changelist'))

    @staticmethod
    @csrf_protect
    @permission_required('media.add_file')
    def bulk_upload(request):
        from django.core.urlresolvers import reverse
        from django.utils.functional import lazy

        def import_zipfile(request, folder_id, data):
            import zipfile
            from os import path

            folder = None
            if folder_id:
                folder = File.objects.get(pk=int(category_id))

            try:
                z = zipfile.ZipFile(data)

                storage = File.fs
                if not storage:
                    messages.error(request, _("Could not access storage"))
                    return

                count = 0
                for zi in z.infolist():
                    if not zi.filename.endswith('/'):
                        from django.template.defaultfilters import slugify
                        from django.core.files.base import ContentFile

                        bname = path.basename(zi.filename)
                        if bname and not bname.startswith(".") and "." in bname:
                            fname, ext = path.splitext(bname)
                            target_fname = slugify(fname) + ext.lower()

                            mf = File()
                            mf.file.save(target_fname, ContentFile(z.read(zi.filename)))
                            mf.save()
#                            if category:
#                                mf.categories.add(category)
                            count += 1

                messages.info(request, _("%d files imported") % count)
            except Exception, e:
                messages.error(request, _("ZIP file invalid: %s") % str(e))
                return

        if request.method == 'POST' and 'data' in request.FILES:
            import_zipfile(request, request.POST.get('category'), request.FILES['data'])
        else:
            messages.error(request, _("No input file given"))

        return HttpResponseRedirect(reverse('webcms_admin:media_file_changelist'))

    def queryset(self, request):
        qs = super(FileAdmin, self).queryset(request)

        # FIXME: This is an ugly hack but it avoids 1-3 queries per *FILE*
        # retrieving the translation information
        if settings.DATABASE_ENGINE == 'postgresql_psycopg2':
            qs = qs.extra(
                select = {
                    'preferred_translation':
                        """SELECT name FROM media_filetranslation
                        WHERE media_filetranslation.parent_id = media_file.id
                        ORDER BY
                            language_code = %s DESC,
                            language_code = %s DESC,
                            LENGTH(language_code) DESC
                        LIMIT 1
                        """
                },
                select_params = (translation.get_language(), settings.LANGUAGE_CODE)
            )
        return qs

    def save_model(self, request, obj, form, change):
        obj.purge_translation_cache()
        return super(FileAdmin, self).save_model(request, obj, form, change)
