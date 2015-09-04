
from leonardo.utils.compatibility import FEINCMS_2


if FEINCMS_2:
    from feincms.extensions.translations import *
else:
    from feincms.module.extensions.translations import *
