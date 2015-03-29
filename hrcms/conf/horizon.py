
from __future__ import absolute_import

HORIZON_CONFIG = {
    # Allow for ordering dashboards; list or tuple if provided.
    'dashboards': ["module", "portal"],

    # Name of a default dashboard; defaults to first alphabetically if None
    'default_dashboard': "portal",

    # Default redirect url for users' home
    'user_home': "",

    # AJAX settings for JavaScript
    'ajax_queue_limit': 10,
    'ajax_poll_interval': 2500,

    # URL for additional help with this site.
    'help_url': None,

    # Exception configuration.
    'exceptions': {'unauthorized': [],
                   'not_found': [],
                   'recoverable': []},

    # Password configuration.
    'password_validator': {'regex': '.*',
                           'help_text': ("Password is not accepted")},

    'password_autocomplete': 'on',

    # Enable or disable simplified floating IP address management.
    'simple_ip_management': True
}
