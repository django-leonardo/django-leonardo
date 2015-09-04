
from leonardo.utils.compatibility import FEINCMS_2


if FEINCMS_2:
    from feincms.extensions.changedate import *
else:
    from feincms.module.extensions.changedate import *
