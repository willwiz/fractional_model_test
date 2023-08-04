# File: HModels.pyx
# distutils: language = c++
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION
# cython: language_level=3
'''
To be written

'''
import numpy as np
cimport numpy as np
cimport cython

cimport src.cython.headers.fractional.caputo
from src.cython.headers.constitutive.neohookean cimport NeoHookean
from src.cython.headers.constitutive.hog_2D cimport Hog2D
from src.cython.headers.constitutive.struc_hog_2D cimport StrucHOG2D
from src.cython.headers.optimization.simulation cimport (
  femoral_he_simulate,
  femoral_ve_simulate,
  thoracic_default_ve_simulate_scaled,
)
from src.cython.headers.optimization.objective cimport (
  femoral_residual_HE,
  femoral_residual_VE,
  thoracic_default_residual_VE_scaled_hyst_relax,
)




cdef extern from "src/cpp/fractional/caputo.hpp" namespace "caputo":
  cdef cppclass caputo_init_4:
    caputo_init_4() except +
    caputo_init_4(double alpha, double Tf, double delta) except +
    double alpha, Tf, delta, beta0
    int N
    double betas[9]
    double taus[9]
    double Q[9*4]
    double f_prev[4]
    void set_pars(double alpha, double Tf, double delta)


# ------------------------------------------------------------------------------
# Caputo Derivative
#
# COMMENT:
# ------------------------------------------------------------------------------

cdef class caputo_initialize:
  cdef caputo_init_4 carp
  def __init__(self, double alpha, double Tf, double delta):
    self.carp = caputo_init_4(alpha, Tf, delta)
  def set_pars(self,  double alpha, double Tf, double delta):
    self.carp.set_pars(alpha, Tf, delta)
  @property
  def beta0(self):
    return self.carp.beta0
  @property
  def betas(self):
    return self.carp.betas
  @property
  def taus(self):
    return self.carp.taus


# ------------------------------------------------------------------------------
# Neohookean
#
# COMMENT:
# ------------------------------------------------------------------------------

cdef class NeoHookean2D:
  cdef NeoHookean model
  def __init__(self, double mu):
    self.model = NeoHookean(mu)
  def set_pars(self, double mu):
    self.model.set_pars(mu)
  def stress(self, np.ndarray[np.float64_t, ndim=1] args):
    cdef np.ndarray[dtype = np.float64_t, ndim=1] sigma = np.zeros(4, dtype=np.float64)
    self.model.stress(&args[0], &sigma[0])
    return sigma


# ------------------------------------------------------------------------------
# Fiber Models
#
# COMMENT:
# ------------------------------------------------------------------------------

cdef class HOGstruc2D:
  cdef StrucHOG2D model
  def __init__(self, double k1, double k2, double theta, double alpha, double beta, double kip, double kop):
    self.model = StrucHOG2D(k1, k2, theta, alpha, beta, kip, kop)
  def set_pars(self, double k1, double k2, double theta, double alpha, double beta, double kip, double kop):
    self.model.set_pars(k1, k2, theta, alpha, beta, kip, kop)
  def stress(self, np.ndarray[np.float64_t, ndim=1] args):
    cdef np.ndarray[dtype = np.float64_t, ndim=1] sigma = np.zeros(4, dtype=np.float64)
    self.model.stress(&args[0], &sigma[0])
    return sigma


cdef class pyHOG2D:
  cdef Hog2D model
  def __init__(self, double k1, double k2, double theta):
    self.model = Hog2D(k1, k2, theta)
  def set_pars(self, double k1, double k2, double theta):
    self.model.set_pars(k1, k2, theta)
  def stress(self, np.ndarray[np.float64_t, ndim=1] args):
    cdef np.ndarray[dtype = np.float64_t, ndim=1] sigma = np.zeros(4, dtype=np.float64)
    self.model.stress(&args[0], &sigma[0])
    return sigma


# ------------------------------------------------------------------------------
# Simulate
#
# COMMENT:
# ------------------------------------------------------------------------------

def Femoral_HESimulation_cpp(double[:] pars, double[:] fiber, double[:] caputo,
                 double Tf, double[:] Cmax, double[:,:] args, double[:] dt):
  n = int(dt.shape[0])
  cdef np.ndarray[dtype = np.float64_t, ndim=2] sigma = np.zeros((n, 4), dtype=np.float64)
  cdef double[:, :] stress = sigma
  femoral_he_simulate(&pars[0], &fiber[0], &caputo[0],
              Tf, &Cmax[0], &args[0][0], &dt[0], &stress[0][0], n)
  return sigma


def Femoral_VESimulation_cpp(double[:] pars, double[:] fiber, double[:] caputo,
                         double Tf, double[:] Cmax, double[:,:] args, double[:] dt):
  n = int(dt.shape[0])
  cdef np.ndarray[dtype = np.float64_t, ndim=2] sigma = np.zeros((n, 4), dtype=np.float64)
  cdef double[:, :] stress = sigma
  femoral_ve_simulate(&pars[0], &fiber[0], &caputo[0],
                      Tf, &Cmax[0], &args[0][0], &dt[0], &stress[0][0], n)
  return sigma




def ThoracicDefault_VESimulation_Scaled_cpp(double[:] pars, double[:] fiber, double[:] caputo,
                                double Tf, double[:] Cmax, double[:,:] args, double[:] dt):
  n = int(dt.shape[0])
  cdef np.ndarray[dtype = np.float64_t, ndim=2] sigma = np.zeros((n, 4), dtype=np.float64)
  cdef double[:, :] stress = sigma
  thoracic_default_ve_simulate_scaled(&pars[0], &fiber[0], &caputo[0],
                             Tf, &Cmax[0], &args[0][0], &dt[0], &stress[0][0], n)
  return sigma

# ------------------------------------------------------------------------------
# Residual Functions
#
# COMMENT:
# ------------------------------------------------------------------------------

def Femoral_ResidualFun_HE_cpp(
  double[:] pars, double[:] fiber,
  double[:] caputo, double Tf, double[:] Cmax,
  double[:,:] strain, double[:,:] stress, double[:] dt, double[:,:] weights,
  double[:,:] deltaCG, double[:,:] hysteresis, double[:] alpha,
  int[:] index, int[:] select, int skip = 1
):
  n     = int(strain.shape[0])
  dim   = int(strain.shape[1])
  nprot = int(select.shape[0])
  return femoral_residual_HE(&pars[0], &fiber[0],
    &caputo[0], Tf, &Cmax[0],
    &strain[0][0], &stress[0][0], &dt[0], &weights[0][0],
    &deltaCG[0][0], &hysteresis[0][0], &alpha[0],
    &index[0], &select[0], n, dim, nprot, int(skip))



def Femoral_ResidualFun_VE_cpp(
  double[:] pars, double[:] fiber,
  double[:] caputo, double Tf, double[:] Cmax,
  double[:,:] strain, double[:,:] stress, double[:] dt, double[:,:] weights,
  double[:,:] deltaCG, double[:,:] hysteresis, double[:] alpha,
  int[:] index, int[:] select, int skip = 1
):
  n     = int(strain.shape[0])
  dim   = int(strain.shape[1])
  nprot = int(select.shape[0])
  return femoral_residual_VE(&pars[0], &fiber[0],
    &caputo[0], Tf, &Cmax[0],
    &strain[0][0], &stress[0][0], &dt[0], &weights[0][0],
    &deltaCG[0][0], &hysteresis[0][0], &alpha[0],
    &index[0], &select[0], n, dim, nprot, int(skip))



def ThoracicDefault_ResidualFun_VE_scaled_hyst_relax_cpp(
  double[:] pars, double[:] fiber,
  double[:] caputo, double Tf, double[:] Cmax,
  double[:,:] strain, double[:,:] stress, double[:] dt, double[:,:] weights,
  double[:,:] deltaCG, double[:,:] hysteresis, double[:] alpha,
  int[:] index, int[:] select, int skip = 1
):
  n     = int(strain.shape[0])
  dim   = int(strain.shape[1])
  nprot = int(select.shape[0])
  return thoracic_default_residual_VE_scaled_hyst_relax(&pars[0], &fiber[0],
    &caputo[0], Tf, &Cmax[0],
    &strain[0][0], &stress[0][0], &dt[0], &weights[0][0],
    &deltaCG[0][0], &hysteresis[0][0], &alpha[0],
    &index[0], &select[0], n, dim, nprot, int(skip))
