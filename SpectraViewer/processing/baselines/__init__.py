from __future__ import absolute_import
import warnings

# Import class wrappers for each type of baseline alg.

from .alsOld import ALS_old


BL_CLASSES_2 = dict(ALS_old=ALS_old)
