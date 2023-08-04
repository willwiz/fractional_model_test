# File: templates.pxd
# distutils: language = c++
# cython: language_level=3


""" ----------------------------------------------------------------------------
C++ Source Files
---------------------------------------------------------------------------- """

cimport src.cython.headers.CTvalues_optimization
cimport src.cython.headers.constitutive.interfaces

cdef extern from "src/cpp/optimization/templates.cpp":
  pass

""" ----------------------------------------------------------------------------
End of Source Files
---------------------------------------------------------------------------- """


# ------------------------------------------------------------------------------
# C++ Header files + exported definitions
# ------------------------------------------------------------------------------

cdef extern from "src/cpp/optimization/templates.hpp" namespace "residuals":
  cdef double residual_body(double[] strain, double[] stress, double[] weights,
    int[] index, int[] select, int dim, int nprot, int skip, double[] sims)

