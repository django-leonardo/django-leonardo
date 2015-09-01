
from django.conf import settings

from django.core.files.storage import get_storage_class
from filer.utils.loader import load_object
from filer.utils.recursive_dictionary import RecursiveDictionaryWithExcludes
import os



# File download permissions are an experimental
# feature. The api may change at any time.
MEDIA_ENABLE_PERMISSIONS = getattr(settings, 'MEDIA_ENABLE_PERMISSIONS', True)
MEDIA_IS_PUBLIC_DEFAULT = getattr(settings, 'MEDIA_IS_PUBLIC_DEFAULT', True)
MEDIA_PUBLIC_UPLOAD_TO = getattr(settings, 'MEDIA_PUBLIC_UPLOAD_TO', 'public')
MEDIA_PRIVATE_UPLOAD_TO = getattr(settings, 'MEDIA_PRIVATE_UPLOAD_TO', 'private')
MEDIA_PAGINATE_BY = getattr(settings, 'MEDIA_PAGINATE_BY', 25)
MEDIA_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS = getattr(settings, 'MEDIA_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS', False)

MEDIA_IMAGE_MODEL = getattr(settings, 'MEDIA_IMAGE_MODEL', False)
# This is an ordered iterable that describes a list of
# classes that I should check for when adding files
MEDIA_FILE_MODELS = getattr(settings, 'MEDIA_FILE_MODELS',
    (
        MEDIA_IMAGE_MODEL if MEDIA_IMAGE_MODEL else 'leonardo.module.media.models.Image',
        'leonardo.module.media.models.File',
        'leonardo.module.media.models.Document',
        'leonardo.module.media.models.Video',
        'leonardo.module.media.models.Vector',
    )
)

DEFAULT_FILE_STORAGE = getattr(settings, 'DEFAULT_FILE_STORAGE', 'django.core.files.storage.FileSystemStorage')


DEFAULT_MEDIA_STORAGES = {
    'public': {
        'main': {
            'ENGINE': DEFAULT_FILE_STORAGE,
            'OPTIONS': {
                'location': os.path.abspath(os.path.join(settings.MEDIA_ROOT)),
                'base_url': '/media/',
            },
            'UPLOAD_TO': 'filer.utils.generate_filename.by_date',
            'UPLOAD_TO_PREFIX': MEDIA_PUBLIC_UPLOAD_TO,
        },
        'thumbnails': {
            'ENGINE': DEFAULT_FILE_STORAGE,
            'OPTIONS': {},
            'THUMBNAIL_OPTIONS': {
                'base_dir': 'public_thumbnails',
            },
        },
    },
    'private': {
        'main': {
            'ENGINE': 'filer.storage.PrivateFileSystemStorage',
            'OPTIONS': {
                'location': os.path.abspath(os.path.join(settings.MEDIA_ROOT)),
                'base_url': '/smedia/',
            },
            'UPLOAD_TO': 'filer.utils.generate_filename.by_date',
            'UPLOAD_TO_PREFIX': MEDIA_PRIVATE_UPLOAD_TO,
        },
        'thumbnails': {
            'ENGINE': 'filer.storage.PrivateFileSystemStorage',
            'OPTIONS': {
                'location': os.path.abspath(os.path.join(settings.MEDIA_ROOT, MEDIA_PRIVATE_UPLOAD_TO)),
                'base_url': '/smedia/private_thumbnails/',
            },
            'THUMBNAIL_OPTIONS': {},
        },
    },
}

# OLD FILER STUFF

DEFAULT_FILER_STORAGES = DEFAULT_MEDIA_STORAGES

FILER_IMAGE_MODEL = MEDIA_IMAGE_MODEL
FILER_ENABLE_PERMISSIONS = MEDIA_ENABLE_PERMISSIONS
FILER_DEBUG = getattr(settings, 'FILER_DEBUG', False) # When True makes
FILER_SUBJECT_LOCATION_IMAGE_DEBUG = getattr(settings, 'FILER_SUBJECT_LOCATION_IMAGE_DEBUG', False)
FILER_WHITESPACE_COLOR = getattr(settings, 'FILER_WHITESPACE_COLOR', '#FFFFFF')

FILER_ENABLE_LOGGING = getattr(settings, 'FILER_ENABLE_LOGGING', False)
if FILER_ENABLE_LOGGING:
    FILER_ENABLE_LOGGING = (FILER_ENABLE_LOGGING and (getattr(settings,'LOGGING') and
                                                      ('' in settings.LOGGING['loggers'] or
                                                       'filer' in settings.LOGGING['loggers'])))

FILER_IS_PUBLIC_DEFAULT = MEDIA_IS_PUBLIC_DEFAULT

FILER_PAGINATE_BY = MEDIA_PAGINATE_BY

FILER_STATICMEDIA_PREFIX = getattr(settings, 'FILER_STATICMEDIA_PREFIX', None)
if not FILER_STATICMEDIA_PREFIX:
    FILER_STATICMEDIA_PREFIX = (getattr(settings, 'STATIC_URL', None) or settings.MEDIA_URL) + 'filer/'

MEDIA_ADMIN_ICON_SIZES = getattr(settings,"MEDIA_ADMIN_ICON_SIZES",(
    '16', '32', '48', '64',
    ))
FILER_ADMIN_ICON_SIZES = MEDIA_ADMIN_ICON_SIZES

THUMBNAIL_HIGH_RESOLUTION = True

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

FILER_FILE_MODELS = MEDIA_FILE_MODELS

MINIMAL_FILER_STORAGES = {
    'public': {
        'main': {
            'ENGINE': None,
            'OPTIONS': {},
            },
        'thumbnails': {
            'ENGINE': None,
            'OPTIONS': {},
            }
    },
    'private': {
        'main': {
            'ENGINE': None,
            'OPTIONS': {},
            },
        'thumbnails': {
            'ENGINE': None,
            'OPTIONS': {},
            },
        },
    }

MINIMAL_FILER_SERVERS = {
    'private': {
        'main': {
            'ENGINE': None,
            'OPTIONS': {},
        },
        'thumbnails': {
            'ENGINE': None,
            'OPTIONS': {},
        },
    },
}

DEFAULT_FILER_SERVERS = {
    'private': {
        'main': {
            'ENGINE': 'filer.server.backends.default.DefaultServer',
            'OPTIONS': {},
        },
        'thumbnails': {
            'ENGINE': 'filer.server.backends.default.DefaultServer',
            'OPTIONS': {},
        },
    },
}

FILER_STORAGES = RecursiveDictionaryWithExcludes(MINIMAL_FILER_STORAGES, rec_excluded_keys=('OPTIONS', 'THUMBNAIL_OPTIONS'))

user_filer_storages = getattr(settings, 'FILER_STORAGES', {})

FILER_STORAGES.rec_update(user_filer_storages)

def update_storage_settings(user_settings, defaults, s, t):
    if not user_settings[s][t]['ENGINE']:
        user_settings[s][t]['ENGINE'] = defaults[s][t]['ENGINE']
        user_settings[s][t]['OPTIONS'] = defaults[s][t]['OPTIONS']
    if t == 'main':
        if not 'UPLOAD_TO' in user_settings[s][t]:
            user_settings[s][t]['UPLOAD_TO'] = defaults[s][t]['UPLOAD_TO']
        if not 'UPLOAD_TO_PREFIX' in user_settings[s][t]:
            user_settings[s][t]['UPLOAD_TO_PREFIX'] = defaults[s][t]['UPLOAD_TO_PREFIX']
    if t == 'thumbnails':
        if not 'THUMBNAIL_OPTIONS' in user_settings[s][t]:
            user_settings[s][t]['THUMBNAIL_OPTIONS'] = defaults[s][t]['THUMBNAIL_OPTIONS']
    return user_settings

update_storage_settings(FILER_STORAGES, DEFAULT_FILER_STORAGES, 'public', 'main')
update_storage_settings(FILER_STORAGES, DEFAULT_FILER_STORAGES, 'public', 'thumbnails')
update_storage_settings(FILER_STORAGES, DEFAULT_FILER_STORAGES, 'private', 'main')
update_storage_settings(FILER_STORAGES, DEFAULT_FILER_STORAGES, 'private', 'thumbnails')

FILER_SERVERS = RecursiveDictionaryWithExcludes(MINIMAL_FILER_SERVERS, rec_excluded_keys=('OPTIONS',))
FILER_SERVERS.rec_update(getattr(settings, 'FILER_SERVERS', {}))

def update_server_settings(settings, defaults, s, t):
    if not settings[s][t]['ENGINE']:
        settings[s][t]['ENGINE'] = defaults[s][t]['ENGINE']
        settings[s][t]['OPTIONS'] = defaults[s][t]['OPTIONS']
    return settings

update_server_settings(FILER_SERVERS, DEFAULT_FILER_SERVERS, 'private', 'main')
update_server_settings(FILER_SERVERS, DEFAULT_FILER_SERVERS, 'private', 'thumbnails')



# Public media (media accessible without any permission checks)
FILER_PUBLICMEDIA_STORAGE = get_storage_class(FILER_STORAGES['public']['main']['ENGINE'])(**FILER_STORAGES['public']['main']['OPTIONS'])
FILER_PUBLICMEDIA_UPLOAD_TO = load_object(FILER_STORAGES['public']['main']['UPLOAD_TO'])
if 'UPLOAD_TO_PREFIX' in FILER_STORAGES['public']['main']:
    FILER_PUBLICMEDIA_UPLOAD_TO = load_object('filer.utils.generate_filename.prefixed_factory')(FILER_PUBLICMEDIA_UPLOAD_TO, FILER_STORAGES['public']['main']['UPLOAD_TO_PREFIX'])
FILER_PUBLICMEDIA_THUMBNAIL_STORAGE = get_storage_class(FILER_STORAGES['public']['thumbnails']['ENGINE'])(**FILER_STORAGES['public']['thumbnails']['OPTIONS'])
FILER_PUBLICMEDIA_THUMBNAIL_OPTIONS = FILER_STORAGES['public']['thumbnails']['THUMBNAIL_OPTIONS']


# Private media (media accessible through permissions checks)
FILER_PRIVATEMEDIA_STORAGE = get_storage_class(FILER_STORAGES['private']['main']['ENGINE'])(**FILER_STORAGES['private']['main']['OPTIONS'])
FILER_PRIVATEMEDIA_UPLOAD_TO = load_object(FILER_STORAGES['private']['main']['UPLOAD_TO'])
if 'UPLOAD_TO_PREFIX' in FILER_STORAGES['private']['main']:
    FILER_PRIVATEMEDIA_UPLOAD_TO = load_object('filer.utils.generate_filename.prefixed_factory')(FILER_PRIVATEMEDIA_UPLOAD_TO, FILER_STORAGES['private']['main']['UPLOAD_TO_PREFIX'])
FILER_PRIVATEMEDIA_THUMBNAIL_STORAGE = get_storage_class(FILER_STORAGES['private']['thumbnails']['ENGINE'])(**FILER_STORAGES['private']['thumbnails']['OPTIONS'])
FILER_PRIVATEMEDIA_THUMBNAIL_OPTIONS = FILER_STORAGES['private']['thumbnails']['THUMBNAIL_OPTIONS']
FILER_PRIVATEMEDIA_SERVER = load_object(FILER_SERVERS['private']['main']['ENGINE'])(**FILER_SERVERS['private']['main']['OPTIONS'])
FILER_PRIVATEMEDIA_THUMBNAIL_SERVER = load_object(FILER_SERVERS['private']['thumbnails']['ENGINE'])(**FILER_SERVERS['private']['thumbnails']['OPTIONS'])

FILER_DUMP_PAYLOAD = getattr(settings, 'FILER_DUMP_PAYLOAD', False)  # Whether the filer shall dump the files payload
