
from .foldermodels import Folder, FolderPermission  # noqa
from .imagemodels import Image  # noqa
from .filemodels import File  # noqa
from .clipboardmodels import Clipboard, ClipboardItem  # noqa
from .virtualitems import *
from .media import *

MEDIA_MODELS = [Image, Document, Vector, Video, Flash, File]
