# File: femoral_model.pxd
# distutils: language = c++
# cython: language_level=3


""" ----------------------------------------------------------------------------
C++ Source Files
---------------------------------------------------------------------------- """

cimport cython.headers.fractional.fractional
cimport cython.headers.constitutive.hog_2D
cimport cython.headers.kinematics.kinematics
cimport cython.headers.constitutive.interfaces
cimport cython.headers.CTvalues_optimization
cimport cython.headers.constitutive.struc_hog_2D
cimport cython.headers.constitutive.neohookean

cdef extern from "cpp/tissue_models/femoral_model.cpp":
  pass

""" ----------------------------------------------------------------------------
End of Source Files
---------------------------------------------------------------------------- """


# ------------------------------------------------------------------------------
# C++ Header files + exported definitions
# ------------------------------------------------------------------------------

cdef extern from "cpp/tissue_models/femoral_model.hpp" namespace "sim":
  cdef cppclass Femoral:
    Femoral(double[] pars, double[] fiber) except +
    Femoral(double[] pars, double[] fiber, double[] Cmax) except +
    void get_scaled_pars(double[] pars)

  cdef cppclass FemoralVE:
    FemoralVE(double[] pars, double[] fiber, double[] visco, double Tf) except +
    FemoralVE(double[] pars, double[] fiber, double[] visco, double Tf,
      double[] Cmax) except +
