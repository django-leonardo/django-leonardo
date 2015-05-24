
===============
Django-Leonardo
===============

A collection of awesome Django libraries, resources and shiny things.
Full featured framework for building everything based on Django, FeinCMS, Horizon, Oscar and tons of another apps.

Why
===

Python and Django communities are dynamic. Django is best framework for building web applications with tons apps, which provide additional futures. If you want make new web site really quick you must spend a lot of time for searching right libraries, integrating and configuring. Leonardo provide new module system which makes this much more easier than before. Leonardo solves cms, graph domains and provide stable core for easy extending and building whatever.

How it works
============

Leonardo loads all modules and gather their stuff. Extending is provided via consistent API which mirror settings of libraries and applications on which is based. Leonardo merge all keys securelly without duplicities.

Last thing in setup process is loading all stuff from ``local_settings``.

These provide new features for us

* no app settings required
* one ``manage.py`` etc..
* app dependencies::

    apps = [
        'leonardo_bootswatch',
        'leonardo_analytics', # this can be defined in other applications
    ]

* autoinclude (Leonardo adds all Leonardo Modules to ``INSTALLED_APPS``)