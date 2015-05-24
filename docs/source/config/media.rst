
===============
Storage / Media
===============

In this time we have good integration of Django-Filer, which provides good base for us.

We support for standard scenarious:

* make, upload, delete, move folders and files
* import files (scan) into concrete folder via admin or command
* basic media entities


Configuation
============

put your configuation into your ``local_settings.py``, these is defaults, you can also update only one concrete field, but you must import default from ``leonardo.module.media.settings``

.. code-block:: python
    
    FILER_ENABLE_PERMISSIONS = True

    FILER_STORAGES = {
        'public': {
            'main': {
                'ENGINE': 'filer.storage.PublicFileSystemStorage',
                'OPTIONS': {
                    'location': '/path/to/media/filer',
                    'base_url': '/smedia/filer/',
                },
                'UPLOAD_TO': 'filer.utils.generate_filename.randomized',
                'UPLOAD_TO_PREFIX': 'filer_public',
            },
            'thumbnails': {
                'ENGINE': 'filer.storage.PublicFileSystemStorage',
                'OPTIONS': {
                    'location': '/path/to/media/filer_thumbnails',
                    'base_url': '/smedia/filer_thumbnails/',
                },
            },
        },
        'private': {
            'main': {
                'ENGINE': 'filer.storage.PrivateFileSystemStorage',
                'OPTIONS': {
                    'location': '/path/to/smedia/filer',
                    'base_url': '/smedia/filer/',
                },
                'UPLOAD_TO': 'filer.utils.generate_filename.randomized',
                'UPLOAD_TO_PREFIX': 'filer_public',
            },
            'thumbnails': {
                'ENGINE': 'filer.storage.PrivateFileSystemStorage',
                'OPTIONS': {
                    'location': '/path/to/smedia/filer_thumbnails',
                    'base_url': '/smedia/filer_thumbnails/',
                },
            },
        },
    }

Imports
=======

.. code-block:: python

    manage.py import_files --path=/tmp/assets/images
    manage.py import_files --path=/tmp/assets/news --folder=images


.. note::

    via admin we support only relative(``MEDIA_ROOT``) scan