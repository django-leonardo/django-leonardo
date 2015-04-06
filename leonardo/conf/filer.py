
THUMBNAIL_HIGH_RESOLUTION = True

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

# File download permissions are an experimental
# feature. The api may change at any time.

FILER_ENABLE_PERMISSIONS = True

"""
FILER_STORAGES = {
    'public': {
        'main': {
            'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': MEDIA_ROOT,
                'base_url': MEDIA_URL,
            },
            'UPLOAD_TO': 'filer.utils.generate_filename.randomized',
        },
        'thumbnails': {
            'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': MEDIA_ROOT,
                'base_url': MEDIA_URL,
            },
        },
    },
    'private': {
        'main': {
            'ENGINE': 'filer.storage.PrivateFileSystemStorage',
            'OPTIONS': {
                'location': MEDIA_ROOT + 'filer',
                'base_url': MEDIA_URL + 'filer/',
            },
            'UPLOAD_TO': 'filer.utils.generate_filename.randomized',
        },
        'thumbnails': {
            'ENGINE': 'filer.storage.PrivateFileSystemStorage',
            'OPTIONS': {
                'location': MEDIA_ROOT + 'filer_thumbnails',
                'base_url': MEDIA_URL + 'filer_thumbnails/',
            },
        },
    },
}
"""