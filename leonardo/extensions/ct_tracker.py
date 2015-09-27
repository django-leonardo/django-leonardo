
from leonardo.utils.compatibility import FEINCMS_2


if FEINCMS_2:
    from feincms.extensions.ct_tracker import *
else:
    from feincms.module.extensions.ct_tracker import *
