
import os
from datetime import datetime

from django.conf import settings
from django.contrib.auth import models as auth_models
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.timezone import get_current_timezone, make_aware, now
from django.utils.translation import ugettext_lazy as _
from feincms.module.page.extensions.navigation import (NavigationExtension,
                                                       PagePretender)
from filer import settings as filer_settings
from filer.models.abstract import BaseImage
from filer.models.filemodels import File
from filer.models.foldermodels import Folder
from filer.utils.compatibility import python_2_unicode_compatible


class MediaMixin(object):

    @classmethod
    def matches_file_type(cls, iname, ifile=None, request=None):
        # the extensions we'll recognise for this file type
        # (majklk): TODO move to settings or live config
        filename_extensions = getattr(cls, 'filename_extensions', '*')
        ext = os.path.splitext(iname)[1].lower()
        return ext in filename_extensions


class LeonardoFolder(Folder):

    class Meta:
        verbose_name = ("folder")
        verbose_name_plural = ('folders')
        app_label = 'media'


class Document(MediaMixin, File):

    filename_extensions = ['.pdf', '.xls', ]

    class Meta:
        verbose_name = ("document")
        verbose_name_plural = ('documents')


class Vector(MediaMixin, File):

    filename_extensions = ['.svg', '.eps', ]

    class Meta:
        verbose_name = ("vector")
        verbose_name_plural = ('vetors')


class Video(MediaMixin, File):

    filename_extensions = ['.dv', '.mov', '.mp4', '.avi', '.wmv', ]

    class Meta:
        verbose_name = ("video")
        verbose_name_plural = ('videos')


class Flash(MediaMixin, File):

    filename_extensions = ['.swf']

    class Meta:
        verbose_name = ("flash video")
        verbose_name_plural = ('flash videos')


class Image(MediaMixin, BaseImage):

    filename_extensions = ['.jpg', '.jpeg', '.png', '.gif', ]

    date_taken = models.DateTimeField(_('date taken'), null=True, blank=True,
                                      editable=False)

    author = models.CharField(
        _('author'), max_length=255, null=True, blank=True)

    must_always_publish_author_credit = models.BooleanField(
        _('must always publish author credit'), default=False)
    must_always_publish_copyright = models.BooleanField(
        _('must always publish copyright'), default=False)

    def save(self, *args, **kwargs):
        if self.date_taken is None:
            try:
                exif_date = self.exif.get('DateTimeOriginal', None)
                if exif_date is not None:
                    d, t = exif_date.split(" ")
                    year, month, day = d.split(':')
                    hour, minute, second = t.split(':')
                    if getattr(settings, "USE_TZ", False):
                        tz = get_current_timezone()
                        self.date_taken = make_aware(datetime(
                            int(year), int(month), int(day),
                            int(hour), int(minute), int(second)), tz)
                    else:
                        self.date_taken = datetime(
                            int(year), int(month), int(day),
                            int(hour), int(minute), int(second))
            except Exception:
                pass
        if self.date_taken is None:
            self.date_taken = now()
        super(Image, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _('images')

        # You must define a meta with en explicit app_label
        app_label = 'media'


class FolderPermissionManager(models.Manager):

    """
    Theses methods are called by introspection from "has_generic_permisison" on
    the folder model.
    """

    def get_read_id_list(self, user):
        """
        Give a list of a Folders where the user has read rights or the string
        "All" if the user has all rights.
        """
        return self.__get_id_list(user, "can_read")

    def get_edit_id_list(self, user):
        return self.__get_id_list(user, "can_edit")

    def get_add_children_id_list(self, user):
        return self.__get_id_list(user, "can_add_children")

    def __get_id_list(self, user, attr):
        if user.is_superuser or not filer_settings.FILER_ENABLE_PERMISSIONS:
            return 'All'
        allow_list = set()
        deny_list = set()
        group_ids = user.groups.all().values_list('id', flat=True)
        q = Q(user=user) | Q(group__in=group_ids) | Q(everybody=True)
        perms = self.filter(q).order_by('folder__tree_id', 'folder__level',
                                        'folder__lft')
        for perm in perms:
            p = getattr(perm, attr)

            if p is None:
                # Not allow nor deny, we continue with the next permission
                continue

            if not perm.folder:
                assert perm.type == FolderPermission.ALL

                if p == FolderPermission.ALLOW:
                    allow_list.update(Folder.objects.all().values_list('id', flat=True))
                else:
                    deny_list.update(Folder.objects.all().values_list('id', flat=True))

                continue

            folder_id = perm.folder.id

            if p == FolderPermission.ALLOW:
                allow_list.add(folder_id)
            else:
                deny_list.add(folder_id)

            if perm.type == FolderPermission.CHILDREN:
                if p == FolderPermission.ALLOW:
                    allow_list.update(
                        perm.folder.get_descendants().values_list('id', flat=True))
                else:
                    deny_list.update(
                        perm.folder.get_descendants().values_list('id', flat=True))

        # Deny has precedence over allow
        return allow_list - deny_list


@python_2_unicode_compatible
class FolderPermission(models.Model):
    ALL = 0
    THIS = 1
    CHILDREN = 2

    ALLOW = 1
    DENY = 0

    TYPES = (
        (ALL, _('all items')),
        (THIS, _('this item only')),
        (CHILDREN, _('this item and all children')),
    )

    PERMISIONS = (
        (ALLOW, _('allow')),
        (DENY, _('deny')),
    )

    folder = models.ForeignKey(LeonardoFolder, verbose_name=('folder'), null=True, blank=True,
                               related_name="media_folder_permissions")

    type = models.SmallIntegerField(_('type'), choices=TYPES, default=ALL)
    user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
                             related_name="media_folder_permissions",
                             verbose_name=_("user"), blank=True, null=True)
    group = models.ForeignKey(auth_models.Group,
                              related_name="media_folder_permissions",
                              verbose_name=_("group"), blank=True, null=True)
    everybody = models.BooleanField(_("everybody"), default=False)

    can_edit = models.SmallIntegerField(
        _("can edit"), choices=PERMISIONS, blank=True, null=True, default=None)
    can_read = models.SmallIntegerField(
        _("can read"), choices=PERMISIONS, blank=True, null=True, default=None)
    can_add_children = models.SmallIntegerField(
        _("can add children"), choices=PERMISIONS, blank=True, null=True, default=None)

    objects = FolderPermissionManager()

    def __str__(self):
        if self.folder:
            name = '%s' % self.folder
        else:
            name = 'All Folders'

        ug = []
        if self.everybody:
            ug.append('Everybody')
        else:
            if self.group:
                ug.append("Group: %s" % self.group)
            if self.user:
                ug.append("User: %s" % self.user)
        usergroup = " ".join(ug)
        perms = []
        for s in ['can_edit', 'can_read', 'can_add_children']:
            perm = getattr(self, s)
            if perm == self.ALLOW:
                perms.append(s)
            elif perm == self.DENY:
                perms.append('!%s' % s)
        perms = ', '.join(perms)
        return "Folder: '%s'->%s [%s] [%s]" % (
            name, self.get_type_display(),
            perms, usergroup)

    def clean(self):
        if self.type == self.ALL and self.folder:
            raise ValidationError('Folder cannot be selected with type "all items".')
        if self.type != self.ALL and not self.folder:
            raise ValidationError(
                'Folder has to be selected when type is not "all items".')
        if self.everybody and (self.user or self.group):
            raise ValidationError(
                'User or group cannot be selected together with "everybody".')
        if not self.user and not self.group and not self.everybody:
            raise ValidationError(
                'At least one of user, group, or "everybody" has to be selected.')

    class Meta:
        verbose_name = _('folder permission')
        verbose_name_plural = _('folder permissions')
        app_label = 'media'


class MediaCategoriesNavigationExtension(NavigationExtension):
    name = _('All media categories')

    def children(self, page, **kwargs):
        base_url = page.get_absolute_url()
        category_list = Folder.objects.filter(parent=None)
        for category in category_list:
            subchildren = []
            for subcategory in category.children.all():
                subchildren.append(PagePretender(
                    title=subcategory,
                    url='%s%s/%s/' % (base_url, category.name, subcategory.name),
                    level=5
                ))
            yield PagePretender(
                title=category,
                url='%s%s/' % (base_url, category.name),
                children=subchildren,
                level=5
            )
