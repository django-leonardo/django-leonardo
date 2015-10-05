from ..models import Image
from .utils import FileField, FileMultipleField


class ImageField(FileField):
    model = Image


class ImageMultipleField(FileMultipleField):
    model = Image
