
from .models import Folder, MEDIA_MODELS


def handle_uploaded_file(file, folder=None, is_public=True):
    '''handle uploaded files to folder

    match first media type and returns it
    '''
    _folder = None

    if folder:
        _folder, folder_created = Folder.objects.get_or_create(
            name=folder)

    for cls in MEDIA_MODELS:
        if cls.matches_file_type(file.name):

            obj, created = cls.objects.get_or_create(
                original_filename=file.name,
                file=file,
                folder=_folder,
                is_public=is_public)

            if created:
                return obj

    return None
