
"""Example site bootstrap format
"""

BOOTSTRAP = {

    'auth.User': {
        'admin': {
            'password': 'root',
            'mail': 'root@admin.cz',
        }
    },

    'web.Page': {

        'QuickStart': {

            'title': 'Quickstart',
            'slug': 'quickstart',
            'override_url': '/',
            'featured': False,
            'theme': '__first__',
            'in_navigation': True,
            'active': True,
            'color_scheme': '__first__',

            'content': {

                'header': {
                    'web.SiteHeadingWidget': {
                        'attrs': {
                            'site_title': 'Leonardo Site',
                            'content_theme': 'navbar',
                            'base_theme': 'default',
                        },
                        'dimenssions': {
                            'md': 2
                        },
                    },
                    'web.TreeNavigationWidget': {
                        'attrs': {
                            'depth': 2,
                            'content_theme': 'navbar',
                            'base_theme': 'default',
                        },
                        'dimenssions': {
                            'md': 6
                        },
                    },

                    'web.UserLoginWidget': {
                        'attrs': {
                            'inline': True,
                            'type': 2,
                            'content_theme': 'navbar',
                            'base_theme': 'default',
                        },
                        'dimenssions': {
                            'md': 4
                        },
                    }
                }
            }
        }
    }
}