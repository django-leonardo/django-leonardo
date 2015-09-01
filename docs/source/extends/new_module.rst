
===============
Leonardo Module
===============

Leonardo module is standard Django application with many additional posibilities. In Leonardo module just type your needs and develop your application.

start module directory structure::

    leonardo_module_blog
        |-- __init__.py
        |-- settings.py

Application
-----------

As Django documentations says, you can define your apps in ``apps.py`` or anywhere, in Leonardo we use __init__.py for simplicity. But you can define it where you want.

Redirect configurations to any other location, like::

    # Django stuff
    default_app_config = 'leonardo_module_blog.apps.BlogConfig'
    leonardo_module_conf = 'leonardo_module_blog.apps'

Required setup for Django Application are defined ``AppConfig`` which has basic attributes described in Django Documentation. For Leonardo Module are required one options with prefix ``LEONARDO`` or ``default`` attribute which specify Leonardo Module stuff.

.. code-block:: python

    from django.apps import AppConfig

    default_app_config = 'leonardo_module_blog.BlogConfig'

    class Default(object):

        optgroup = 'Blog'

        apps = [
            'leonardo_module_blog',
            'elephantblog',
            'leonardo_module_analytics',
        ]

        js_files = [
            'js/redactor.js'
        ]

        css_files = [
            'css/redactor.css'
        ]

        config = {
            'BLOG_PAGINATE_BY': (10, _('Blog Entries Pagination')),
            'DISQUS_COMMENTS': (False, _('Enable Disqus comments')),
            'DISQUS_SHORTNAME': ('michaelkuty', _('Disqus shortname identificator.')),

        }

        navigation_extensions = [
            'elephantblog.navigation_extensions.treeinfo',
        ]

        absolute_url_overrides = {
            'elephantblog.entry': 'leonardo_store.overrides.elephantblog_entry_url_app',
            'elephantblog.categorytranslation':
            'leonardo_store.overrides.elephantblog_categorytranslation_url_app',
        }


    # standard django Application
    class BlogConfig(AppConfig, Default):
        name = 'leonardo_module_blog'
        verbose_name = ("Blog")

    default = Default()  # define module configuration

That's all.. Leonardo go throught every module defined in your ``APPS`` and merge all items to main settings file. Complete reference you can see below.

.. note::

	Leonardo supports two syntax. One Pythonic way which is described upstair. ``default`` attribute which respect simple Python Object.

For some users are Python way unnecessarily complicated, for this people leonardo supports another config syntax::

    LEONARDO_APPS = ['app1']

    LEONARDO_ABSOLUTE_URL_OVERRIDES = {
        'elephantblog.entry': 'leonardo_store.overrides.elephantblog_entry_url_app',
        'elephantblog.categorytranslation':
        'leonardo_store.overrides.elephantblog_categorytranslation_url_app',
    }

.. note::

	Just use same keys with prefix and uppercase ``LEONARDO_``

.. tip::

    For all possibility settings keys see Module Reference

Settings
--------

in the settings you may have something like this

.. code-block:: python

    BLOG_TITLE = 'name'

    # whatever

As you expext every key from settings will be inported and merged into main settings file.

.. warning::

    Be careful if you declare keys in the ``module/settings.py``. Every key is imported without special merging process which may override your global settings ! It was designed only for module/app specific defaults.

Release
-------

For releasing big amount of pip packages we use ``PBR`` which was developed for OpenStack and we have tunned version which lives here https://github.com/michaelkuty/pbr.

PBR can and does do a bunch of things for you:

* **Version**: Manage version number based on git revisions and tags
* **AUTHORS**: Generate AUTHORS file from git log
* **ChangeLog**: Generate ChangeLog from git log
* **Sphinx Autodoc**: Generate autodoc stub files for your whole module
* **Requirements**: Store your dependencies in a pip requirements file (install from vcs)
* **long_description**: Use your README file as a long_description
* **Smart find_packages**: Smartly find packages under your root package

With this tool is managing python module pretty simple. Add these lines to your ``setup.py``::

    import setuptools

    # In python < 2.7.4, a lazy loading of package `pbr` will break
    # setuptools if some other modules registered functions in `atexit`.
    # solution from: http://bugs.python.org/issue15881#msg170215
    try:
        import multiprocessing  # noqa
    except ImportError:
        pass

    setuptools.setup(
        setup_requires=['pbr'],
        pbr=True)

and write meta to ``setup.cfg``

.. code-block:: python

    [metadata]
    name = leonardo-team
    summary = Team Application for Leonardo CMS or plain FeinCMS
    description-file =
        README.rst
    author = Michael Kuty
    author-email = kutymichael@gmail.com
    home-page = https://github.com/leonardo-modules/leonardo-team.git
    classifier =
        Development Status :: 5 - Production/Stable
        Framework :: Django
        Intended Audience :: Developers
        License :: OSI Approved :: BSD License
        Operating System :: OS Independent
        Programming Language :: Python
        Programming Language :: Python :: 2.6
        Programming Language :: Python :: 2.7
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3.3
        Programming Language :: Python :: 3.4
        Topic :: Software Development
        Topic :: Software Development :: Libraries :: Application Frameworks

    [files]
    packages =
        team

and run

.. code-block:: bash

    python setup.py sdist register

PBR is GIT driven if you want add new version for release just create new tag like::

    git tag v1.4

and then upload new release to pip::

    python setup.py sdist upload

.. note::

    Full documnetation of PBR lives there http://docs.openstack.org/developer/pbr/