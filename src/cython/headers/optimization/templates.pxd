# File: templates.pxd
# distutils: language = c++
# cython: language_level=3


""" ----------------------------------------------------------------------------
C++ Source Files
---------------------------------------------------------------------------- """

cimport cython.headers.constitutive.interfaces
cimport cython.headers.CTvalues_optimization

cdef extern from "cpp/optimization/templates.cpp":
  pass

""" ----------------------------------------------------------------------------
End of Source Files
---------------------------------------------------------------------------- """


# ------------------------------------------------------------------------------
# C++ Header files + exported definitions
# ------------------------------------------------------------------------------

cdef extern from "cpp/optimization/templates.hpp" namespace "residuals":
  cdef double residual_body(double[] strain, double[] stress, double[] weights,
    int[] index, int[] select, int dim, int nprot, int skip, double[] sims)

