
from django.utils.translation import ugettext_lazy as _
from leonardo import messages
from leonardo.utils import dotdict

from django.core import management

try:
    import github
    GITHUB = True
except Exception:
    GITHUB = False
# github specific
ORG = None

try:
    import pip  # noqa
    PIP = True
except Exception:
    PIP = False


# for this time
# all items for fast search
# in memory ..
REPOS = None
GITHUB_REPOS = None

AVAIL_WIDGETS = None
# hide from search plugin
_BLACKLIST = [
    'django-leonardo',
    'raspiface',
]


def pip_install(packages, request=None, reload_server=False):
    """install packages from pip

    if request is provided, user messages is pushed out
    """

    if PIP:

        # install
        try:
            pip.main(['install'] + list(packages))
            if request:
                messages.success(request, _(
                    'Packages %s was successfully installed,\
                     please restart your server.' % list(packages)))
        except Exception as e:
            if request:
                messages.error(request, _(
                    'Installing packages raised exception %s' % e))
            else:
                raise e
        else:
            if reload_server:
                # try self kill
                try:
                    import os
                    os.kill(os.getpid(), 9)
                except Exception as e:
                    if request:
                        messages.error(request, _(
                            'Run post install task fails with %s' % e))
                    else:
                        raise e

    else:
        if request:
            messages.error(request, _(
                'For this functionality please install pip package'))


def filter_repos():
    """filter repos for duplicity
    """

    global REPOS

    _pkgs = []
    _pkgs_names = []

    if REPOS:

        for item in REPOS:
            if item.name not in _BLACKLIST and item.name not in _pkgs_names:
                _pkgs_names.append(item.name)
                _pkgs.append(item)

        REPOS = _pkgs


def update_global_repos(items):
    """update repos safety
    """

    global REPOS

    if REPOS:
        REPOS += items
    else:
        REPOS = items


def get_widgets(query='leonardo', request=None):
    """returns all widgets
    """
    widgets = {}

    global GITHUB_REPOS

    if GITHUB_REPOS is None:
        update_packages_from_github(query, request)

    if GITHUB:

        for repo in GITHUB_REPOS:

            # TODO read setup.py
            mod_name = repo.name
            raise Exception(mod_name)
            try:
                descriptor = repo.get_file_contents(
                    '%s/__init__.py' % mod_name).decoded_content
            except Exception:
                pass
            else:
                widgets.update({
                    mod_name: descriptor.widgets
                })

        raise Exception(widgets)


def update_packages_from_pip(query, request=None):
    """updates global REPOS from pypi
    """

    if PIP:
        try:
            from pip.commands.search import SearchCommand
            search_results = SearchCommand().search(
                'leonardo', 'https://pypi.python.org/pypi')
            # serialize to dot access dict
            search_results = [dotdict(d) for d in search_results]
        except ImportError:
            if request:
                messages.error(request, _(
                    'For this functionality please install pip package'))
        else:
            update_global_repos(search_results)


def update_packages_from_github(query, request=None):
    """updates global REPOS from leonardo github organization
    """

    global REPOS
    global GITHUB_REPOS

    if GITHUB:
        global ORG

        try:
            g = github.Github()
            org = g.get_organization('leonardo-modules')
        except ImportError:
            if request:
                messages.error(request, _(
                    'For this functionality please run pip install PyGithub'))
        else:
            GITHUB_REPOS = org.get_repos()
            update_global_repos(list(org.get_repos()))
            ORG = org


def update_all(query='leonardo', request=None):

    global REPOS

    if not REPOS:
        update_packages_from_pip(query, request)
        update_packages_from_github(query, request)
        filter_repos()
    return REPOS
