
from leonardo.utils.compatibility import FEINCMS_2


if FEINCMS_2:
    from feincms.extensions.seo import *
else:
    from feincms.module.extensions.seo import *
