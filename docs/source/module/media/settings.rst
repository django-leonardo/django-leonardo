
======================
Advance Media Settings
======================

Leonardo CMS has highly adopted Django-Filer.

``MEDIA_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS``

Regular users are not allowed to create new folders at the root level, only subfolders of already existing folders, unless this setting is set to True

Defaults to ``False``

``MEDIA_PAGINATE_BY``

The number of items (Folders, Files) that should be displayed per page in admin.

Defaults to ``25``

``MEDIA_PUBLIC_UPLOAD_TO``

``MEDIA_PRIVATE_UPLOAD_TO``

``MEDIA_IS_PUBLIC_DEFAULT``

``MEDIA_ENABLE_PERMISSIONS`` - enable permissions

.. warning::

    permissions is only experimental feature


``MEDIA_IMAGE_MODEL`` default is 'leonardo.module.media.models.Image'

Defines the dotted path to a custom Image model; please include the model name. Example: 'my.app.models.CustomImage'


This is an ordered iterable that describes a list of classes that I should check for when adding files

``MEDIA_FILE_MODELS`` = getattr(settings, 'MEDIA_FILE_MODELS',
    (
        MEDIA_IMAGE_MODEL if MEDIA_IMAGE_MODEL else 'leonardo.module.media.models.Image',
        'leonardo.module.media.models.File',
        'leonardo.module.media.models.Document',
        'leonardo.module.media.models.Video',
        'leonardo.module.media.models.Vector',
    )
)