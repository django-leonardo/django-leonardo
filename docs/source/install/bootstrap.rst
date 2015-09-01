
==============
Bootstrap site
==============

We don't repeat yourself and for really quick start with new site we provide simple API called Bootstrap which has simple format in ``yaml`` or ``json`` and may have contains basic stuff for your site::

    auth.User:
      admin:
        password: root
        mail: root@admin.cz
    web.Page:
      QuickStart:
        title: Quickstart
        slug: quickstart
        override_url: /
        featured: false
        theme: __first__
        in_navigation: true
        active: true
        color_scheme: __first__
        content:
          header:
            web.SiteHeadingWidget:
              attrs:
                site_title: Leonardo Site
                content_theme: navbar
                base_theme: default
              dimenssions:
                md: 2
            web.TreeNavigationWidget:
              attrs:
                depth: 2
                content_theme: navbar
                base_theme: default
              dimenssions:
                md: 6
            web.UserLoginWidget:
              attrs:
                inline: true
                type: 2
                content_theme: navbar
                base_theme: default
              dimenssions:
                md: 4
    elephantblog.Entry:
      Test:
        title: Test
        slug: test
        author:
          type: auth.User
          pk: 1
        content:
          main:
            elephantblog.HtmlTextWidget:
              attrs:
                text: Hello world !
                content_theme: default
                base_theme: default
              dimenssions:
                md: 2

From local source

.. code-block:: bash

    python manage.py bootstrap_site --name=demo.yaml

This mechanismus is really simple without any magic features. Just define your model entyties with some parameters. For FeinCMS models is there field called ``content`` which is dictionary of content regions like ``col3`` with some ``Widgets``.

From remote host

.. code-block:: bash

    python manage.py bootstrap_site --url=http://raw.githubusercontent.com/django-leonardo/django-leonardo/develop/contrib/bootstrap/demo.yaml
