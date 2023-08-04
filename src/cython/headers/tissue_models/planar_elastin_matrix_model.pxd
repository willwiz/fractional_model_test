# File: planar_elastin_matrix_model.pxd
# distutils: language = c++
# cython: language_level=3


""" ----------------------------------------------------------------------------
C++ Source Files
---------------------------------------------------------------------------- """

cimport src.cython.headers.constitutive.planar_hog
cimport src.cython.headers.CTvalues_optimization
cimport src.cython.headers.constitutive.neohookean
cimport src.cython.headers.constitutive.interfaces

cdef extern from "src/cpp/tissue_models/planar_elastin_matrix_model.cpp":
  pass

""" ----------------------------------------------------------------------------
End of Source Files
---------------------------------------------------------------------------- """


# ------------------------------------------------------------------------------
# C++ Header files + exported definitions
# ------------------------------------------------------------------------------

cdef extern from "src/cpp/tissue_models/planar_elastin_matrix_model.hpp" namespace "sim":
  cdef cppclass PlanarElastinMatrix:
    PlanarElastinMatrix(double[] pars, double[] fiber, double[] visco, double Tf,
      double[] Cmax) except +
    void get_scaled_pars(double[] pars)

