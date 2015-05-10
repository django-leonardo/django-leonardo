
===================
New Leonardo Module
===================

Leonardo has own layer over Django settings, which provides benefits for easy installation. This text describes how you can create new leonardo module or theme, but is still standard Django app !

Minimal app
===========

Directory structure::

    my_awesome_module
        |-- __init__.py
        |-- settings.py
        |-- urls.py
        |-- views.py

Namespaced Leonardo package
===========================

For extend Leonardo use standard setuptools namespace packages, which provides way for extends big project such as Leonardo.

For full example namespaced module see Leonardo Foo module

https://github.com/leonardo-modules/leonardo-module-foo