
from __future__ import absolute_import

import os

import xstatic.main
import xstatic.pkg.angular
import xstatic.pkg.angular_bootstrap
import xstatic.pkg.angular_gettext
import xstatic.pkg.angular_lrdragndrop
import xstatic.pkg.angular_smart_table
import xstatic.pkg.bootstrap_datepicker
import xstatic.pkg.bootstrap_scss
import xstatic.pkg.d3
import xstatic.pkg.font_awesome
import xstatic.pkg.hogan
import xstatic.pkg.jasmine
import xstatic.pkg.jquery
import xstatic.pkg.jquery_migrate
import xstatic.pkg.jquery_quicksearch
import xstatic.pkg.jquery_tablesorter
import xstatic.pkg.jquery_ui
import xstatic.pkg.jsencrypt
import xstatic.pkg.magic_search
import xstatic.pkg.qunit
import xstatic.pkg.rickshaw
import xstatic.pkg.spin
import xstatic.pkg.termjs
import xstatic.pkg.mdi
import xstatic.pkg.roboto_fontface

from horizon.utils import file_discovery


COMPRESS_PRECOMPILERS = (
    ('text/scss', 'horizon.utils.scss_filter.HorizonScssFilter'),
)

COMPRESS_CSS_FILTERS = (
    'compressor.filters.css_default.CssAbsoluteFilter',
)

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_OUTPUT_DIR = 'compressed'
COMPRESS_CSS_HASHING_METHOD = 'hash'
COMPRESS_PARSER = 'compressor.parser.HtmlParser'
COMPRESS_OFFLINE_CONTEXT = 'leonardo.conf.context.offline_context'

webroot = '/'

STATICFILES_DIRS = [
    ('horizon/lib/angular',
        xstatic.main.XStatic(xstatic.pkg.angular,
                             root_url=webroot).base_dir),
    ('horizon/lib/angular',
        xstatic.main.XStatic(xstatic.pkg.angular_bootstrap,
                             root_url=webroot).base_dir),
    ('horizon/lib/angular',
        xstatic.main.XStatic(xstatic.pkg.angular_gettext,
                             root_url=webroot).base_dir),
    ('horizon/lib/angular',
        xstatic.main.XStatic(xstatic.pkg.angular_lrdragndrop,
                             root_url=webroot).base_dir),
    ('horizon/lib/angular',
        xstatic.main.XStatic(xstatic.pkg.angular_smart_table,
                             root_url=webroot).base_dir),
    ('horizon/lib/bootstrap_datepicker',
        xstatic.main.XStatic(xstatic.pkg.bootstrap_datepicker,
                             root_url=webroot).base_dir),
    ('bootstrap',
        xstatic.main.XStatic(xstatic.pkg.bootstrap_scss,
                             root_url=webroot).base_dir),
    ('horizon/lib',
        xstatic.main.XStatic(xstatic.pkg.d3,
                             root_url=webroot).base_dir),
    ('horizon/lib',
        xstatic.main.XStatic(xstatic.pkg.hogan,
                             root_url=webroot).base_dir),
    ('horizon/lib/font-awesome',
        xstatic.main.XStatic(xstatic.pkg.font_awesome,
                             root_url=webroot).base_dir),
    ('horizon/lib/jasmine',
        xstatic.main.XStatic(xstatic.pkg.jasmine,
                             root_url=webroot).base_dir),
    ('horizon/lib/jquery',
        xstatic.main.XStatic(xstatic.pkg.jquery,
                             root_url=webroot).base_dir),
    ('horizon/lib/jquery',
        xstatic.main.XStatic(xstatic.pkg.jquery_migrate,
                             root_url=webroot).base_dir),
    ('horizon/lib/jquery',
        xstatic.main.XStatic(xstatic.pkg.jquery_quicksearch,
                             root_url=webroot).base_dir),
    ('horizon/lib/jquery',
        xstatic.main.XStatic(xstatic.pkg.jquery_tablesorter,
                             root_url=webroot).base_dir),
    ('horizon/lib/jsencrypt',
        xstatic.main.XStatic(xstatic.pkg.jsencrypt,
                             root_url=webroot).base_dir),
    ('horizon/lib/magic_search',
        xstatic.main.XStatic(xstatic.pkg.magic_search,
                             root_url=webroot).base_dir),
    ('horizon/lib/qunit',
        xstatic.main.XStatic(xstatic.pkg.qunit,
                             root_url=webroot).base_dir),
    ('horizon/lib',
        xstatic.main.XStatic(xstatic.pkg.rickshaw,
                             root_url=webroot).base_dir),
    ('horizon/lib',
        xstatic.main.XStatic(xstatic.pkg.spin,
                             root_url=webroot).base_dir),
    ('horizon/lib/mdi',
     xstatic.main.XStatic(xstatic.pkg.mdi,
                          root_url=webroot).base_dir),
    ('horizon/lib/roboto_fontface',
     xstatic.main.XStatic(xstatic.pkg.roboto_fontface,
                          root_url=webroot).base_dir),
]

if xstatic.main.XStatic(xstatic.pkg.jquery_ui).version.startswith('1.10.'):
    # The 1.10.x versions already contain the 'ui' directory.
    STATICFILES_DIRS.append(('horizon/lib/jquery-ui',
        xstatic.main.XStatic(xstatic.pkg.jquery_ui).base_dir))
else:
    # Newer versions dropped the directory, add it to keep the path the same.
    STATICFILES_DIRS.append(('horizon/lib/jquery-ui/ui',
        xstatic.main.XStatic(xstatic.pkg.jquery_ui).base_dir))

def find_static_files(HORIZON_CONFIG):
    import horizon
    import leonardo
    os_dashboard_home_dir = leonardo.__path__[0]
    horizon_home_dir = horizon.__path__[0]

    # note the path must end in a '/' or the resultant file paths will have a
    # leading "/"
    file_discovery.populate_horizon_config(
        HORIZON_CONFIG,
        os.path.join(horizon_home_dir, 'static/')
    )

    # filter out non-angular javascript code and lib
    HORIZON_CONFIG['js_files'] = ([f for f in HORIZON_CONFIG['js_files']
                                   if not f.startswith('horizon/')])

    # note the path must end in a '/' or the resultant file paths will have a
    # leading "/"
    file_discovery.populate_horizon_config(
        HORIZON_CONFIG,
        os.path.join(os_dashboard_home_dir, 'static/'),
        sub_path='app/'
    )