# File: planar_elastin_matrix_model.pxd
# distutils: language = c++
# cython: language_level=3


""" ----------------------------------------------------------------------------
C++ Source Files
---------------------------------------------------------------------------- """

cimport cython.headers.constitutive.neohookean
cimport cython.headers.constitutive.planar_hog
cimport cython.headers.constitutive.interfaces
cimport cython.headers.CTvalues_optimization

cdef extern from "cpp/tissue_models/planar_elastin_matrix_model.cpp":
  pass

""" ----------------------------------------------------------------------------
End of Source Files
---------------------------------------------------------------------------- """


# ------------------------------------------------------------------------------
# C++ Header files + exported definitions
# ------------------------------------------------------------------------------

cdef extern from "cpp/tissue_models/planar_elastin_matrix_model.hpp" namespace "sim":
  cdef cppclass PlanarElastinMatrix:
    PlanarElastinMatrix(double[] pars, double[] fiber, double[] visco, double Tf,
      double[] Cmax) except +
    void get_scaled_pars(double[] pars)

