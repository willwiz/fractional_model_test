# File: thoracic_default_model.pxd
# distutils: language = c++
# cython: language_level=3


""" ----------------------------------------------------------------------------
C++ Source Files
---------------------------------------------------------------------------- """

cimport src.cython.headers.constitutive.struc_hog_2D
cimport src.cython.headers.CTvalues_optimization
cimport src.cython.headers.constitutive.planar_hog
cimport src.cython.headers.constitutive.neohookean
cimport src.cython.headers.constitutive.hog_2D
cimport src.cython.headers.constitutive.interfaces
cimport src.cython.headers.fractional.fractional

cdef extern from "src/cpp/tissue_models/thoracic_default_model.cpp":
  pass

""" ----------------------------------------------------------------------------
End of Source Files
---------------------------------------------------------------------------- """


# ------------------------------------------------------------------------------
# C++ Header files + exported definitions
# ------------------------------------------------------------------------------

cdef extern from "src/cpp/tissue_models/thoracic_default_model.hpp" namespace "sim":
  cdef cppclass ThoracicDefaultBase:
    ThoracicDefaultBase(double[] pars, double[] fiber) except +
    ThoracicDefaultBase(double[] pars, double[] fiber, double[] Cmax) except +
    void get_scaled_pars(double[] pars)

  cdef cppclass ThoracicDefaultVEBase:
    ThoracicDefaultVEBase(double[] pars, double[] fiber, double[] visco,
      double Tf) except +
    ThoracicDefaultVEBase(double[] pars, double[] fiber, double[] visco,
      double Tf, double[] Cmax) except +

  cdef cppclass ThoracicDefaultVEScaled:
    ThoracicDefaultVEScaled(double[] pars, double[] fiber, double[] visco,
      double Tf, double[] Cmax) except +

