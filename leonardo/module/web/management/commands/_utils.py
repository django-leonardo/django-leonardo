import codecs
import os

from dbtemplates.conf import settings
from dbtemplates.models import Template
from django.contrib.sites.models import Site
from django.template.loaders.app_directories import app_template_dirs

ALWAYS_ASK, FILES_TO_DATABASE, DATABASE_TO_FILES = ('0', '1', '2')


def get_or_create_template(template_name, extension='.html', app_first=False,
                           force=True, delete=False):

    site = Site.objects.get_current()

    if not extension.startswith("."):
        extension = ".%s" % extension

    if app_first:
        tpl_dirs = app_template_dirs + settings.TEMPLATE_DIRS
    else:
        tpl_dirs = settings.TEMPLATE_DIRS + app_template_dirs
    templatedirs = [d for d in tpl_dirs if os.path.isdir(d)]

    for templatedir in templatedirs:
        for dirpath, subdirs, filenames in os.walk(templatedir):
            for f in [f for f in filenames
                      if f.endswith(extension) and not f.startswith(".")]:
                path = os.path.join(dirpath, f)
                name = path.split(templatedir)[1]
                if name.startswith('/'):
                    name = name[1:]
                if template_name in name:
                    try:
                        t = Template.on_site.get(name__exact=name)
                    except Template.DoesNotExist:
                        t = Template(name=name,
                                     content=codecs.open(path, "r").read())
                        t.save()
                        t.sites.add(site)

                    else:
                        if force:
                            t.content = codecs.open(path, 'r').read()
                            t.save()
                            t.sites.add(site)
                            print("{} successfully synced".format(t.name))
                    return t
    return None
