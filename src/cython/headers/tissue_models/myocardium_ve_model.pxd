# File: myocardium_ve_model.pxd
# distutils: language = c++
# cython: language_level=3


""" ----------------------------------------------------------------------------
C++ Source Files
---------------------------------------------------------------------------- """

cimport src.cython.headers.constitutive.myocardium_3D
cimport src.cython.headers.fractional.fractional
cimport src.cython.headers.constitutive.neohookean
cimport src.cython.headers.constitutive.interfaces

cdef extern from "src/cpp/tissue_models/myocardium_ve_model.cpp":
  pass

""" ----------------------------------------------------------------------------
End of Source Files
---------------------------------------------------------------------------- """


# ------------------------------------------------------------------------------
# C++ Header files + exported definitions
# ------------------------------------------------------------------------------

cdef extern from "src/cpp/tissue_models/myocardium_ve_model.hpp" namespace "sim":
  cdef cppclass MyocardiumHE:
    MyocardiumHE(double[] pars, double[] fiber) except +

  cdef cppclass MyocardiumVE:
    MyocardiumVE(double[] pars, double[] fiber, double[] visco, double Tf,
      double[] Cmax) except +

