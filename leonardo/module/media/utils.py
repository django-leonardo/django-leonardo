
from .models import Folder, MEDIA_MODELS


def handle_uploaded_file(file, folder=None, is_public=True):
    '''handle uploaded file to folder
    match first media type and create media object and returns it

    file: File object
    folder: str or Folder isinstance
    is_public: boolean
    '''
    _folder = None

    if folder and isinstance(folder, Folder):
        _folder = folder
    elif folder:
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


def handle_uploaded_files(files, folder=None, is_public=True):
    '''handle uploaded files to folder

    files: array of File objects or single object
    folder: str or Folder isinstance
    is_public: boolean
    '''
    results = []

    for f in files:
        result = handle_uploaded_file(f, folder, is_public)
        results.append(result)
    return results
