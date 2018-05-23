from __future__ import absolute_import, print_function
import numpy as np
from six.moves import xrange

#from .common import WhittakerSmoother, Baseline

# para importar de un padre
import sys
sys.path.insert(0,'..')

# ahora el padre esta en el path y puede usar
from superman.baseline.common import WhittakerSmoother, Baseline 

# Now you can import your module
#from baseline.common import WhittakerSmoother, Baseline 

from scipy.sparse import csc_matrix, spdiags
from scipy.sparse.linalg import spsolve



# esta función es lenta, haz pruebas con otras
#http://stackoverflow.com/questions/29156532/python-baseline-correction-library
# p = asymmetry_param 0.05
# lam = smoothness 100000
def baseline_als(y, lam, p, niter=10):
    L = len(y)
    D = csc_matrix(np.diff(np.eye(L), 2))
    w = np.ones(L)
    for i in range(niter):
        W = spdiags(w, 0, L, L)
        Z = W + lam * D.dot(D.transpose())
        z = spsolve(Z, w*y)
        w = p * (y > z) + (1-p) * (y < z)
    return z

def substract_baseline_als(y, lam, p, niter=10):
    return np.maximum(y-baseline_als(y,lam,p),0)





class ALS_old(Baseline):
  def __init__(self, asymmetry_param=0.01, smoothness_param=1e5, max_iters=10):
    self.asymmetry_ = asymmetry_param
    self.smoothness_ = smoothness_param
    self.max_iters_ = max_iters
    
  # fit_one debería devolver la baseline, no la resta
  def _fit_one(self, bands, intensities):
    #return substract_baseline_als(intensities, self.smoothness_, self.asymmetry_,self.max_iters_)
    return np.minimum(intensities,baseline_als(intensities,self.smoothness_,self.asymmetry_,self.max_iters_))

  def param_ranges(self):
    return {
        'asymmetry_': (1e-3, 1e-1, 'log'),
        'smoothness_': (1e2, 1e8, 'log')
    }
