
COMPRESS_PRECOMPILERS = (
    ('text/scss', 'django_pyscss.compressor.DjangoScssFilter'),
)

COMPRESS_CSS_FILTERS = (
    'compressor.filters.css_default.CssAbsoluteFilter',
)

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = False
COMPRESS_OUTPUT_DIR = 'dashboard'
COMPRESS_CSS_HASHING_METHOD = 'hash'
COMPRESS_PARSER = 'compressor.parser.HtmlParser'

import xstatic.main
import xstatic.pkg.angular
import xstatic.pkg.angular_bootstrap
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
import xstatic.pkg.adminlte
import xstatic.pkg.react

webroot='/'

STATICFILES_DIRS = [
    ('horizon/lib/angular',
        xstatic.main.XStatic(xstatic.pkg.angular,
                             root_url=webroot).base_dir),
    ('horizon/lib/angular',
        xstatic.main.XStatic(xstatic.pkg.angular_bootstrap,
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
    ('horizon/lib',
        xstatic.main.XStatic(xstatic.pkg.termjs,
                             root_url=webroot).base_dir),
    ('lib',
        xstatic.main.XStatic(xstatic.pkg.adminlte).base_dir),
    ('lib',
        xstatic.main.XStatic(xstatic.pkg.react).base_dir),
]

if xstatic.main.XStatic(xstatic.pkg.jquery_ui).version.startswith('1.10.'):
    # The 1.10.x versions already contain the 'ui' directory.
    STATICFILES_DIRS.append(('horizon/lib/jquery-ui',
        xstatic.main.XStatic(xstatic.pkg.jquery_ui).base_dir))
else:
    # Newer versions dropped the directory, add it to keep the path the same.
    STATICFILES_DIRS.append(('horizon/lib/jquery-ui/ui',
        xstatic.main.XStatic(xstatic.pkg.jquery_ui).base_dir))
