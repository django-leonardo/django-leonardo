
import codecs
import os

from dbtemplates.conf import settings
from dbtemplates.models import Template
from django import VERSION
from django.contrib.sites.models import Site
from leonardo.utils.settings import merge

ALWAYS_ASK, FILES_TO_DATABASE, DATABASE_TO_FILES = ('0', '1', '2')

# support for other template backends

DIRS = []

if VERSION[:2] < (1, 8):
    from django.template.loaders.app_directories import app_template_dirs
    DIRS = settings.TEMPLATE_DIRS
else:
    from django.template.utils import get_app_template_dirs
    from django.template.loader import _engine_list
    for engine in _engine_list():
        DIRS.extend(engine.dirs)
    app_template_dirs = get_app_template_dirs('templates')


def get_or_create_template(template_name, extension='.html', app_first=False,
                           force=True, delete=False, prefix='', notfix=None):

    site = Site.objects.get_current()

    if not extension.startswith("."):
        extension = ".%s" % extension

    if app_first:
        tpl_dirs = merge(app_template_dirs, DIRS)
    else:
        tpl_dirs = merge(DIRS, app_template_dirs)
    templatedirs = [d for d in tpl_dirs if os.path.isdir(d)]

    for templatedir in templatedirs:
        for dirpath, subdirs, filenames in os.walk(templatedir):
            for f in [f for f in filenames
                      if f.endswith(extension) and not f.startswith(".")]:
                path = os.path.join(dirpath, f)
                name = path.split(templatedir)[1]
                if name.startswith('/'):
                    name = name[1:]
                if template_name in name and prefix in path:
                    if notfix and notfix in path:
                        continue
                    try:
                        t = Template.on_site.get(name__exact=name)
                    except Template.DoesNotExist:
                        t = Template(name=name,
                                     content=codecs.open(path, "r").read())
                        t.save(sync_themes=False)
                        t.sites.add(site)

                    else:
                        if force:
                            t.content = codecs.open(path, 'r').read()
                            t.save(sync_themes=False)
                            t.sites.add(site)
                    return t
    return None
