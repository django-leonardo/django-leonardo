
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

.. code-block:: bash

    python manage.py bootstrap_site --name=demo.yaml

.. note::

    Examples lives in the ``LEONARDO_BOOTSTRAP_DIR`` which is set to ``leonardo/contrib/bootstrap`` in default state.
