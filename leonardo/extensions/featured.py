
from leonardo.utils.compatibility import FEINCMS_2


if FEINCMS_2:
    from feincms.extensions.featured import *
else:
    from feincms.module.extensions.featured import *
