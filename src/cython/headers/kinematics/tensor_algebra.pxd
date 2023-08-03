# File: tensor_algebra.pxd
# distutils: language = c++
# cython: language_level=3


""" ----------------------------------------------------------------------------
C++ Source Files
---------------------------------------------------------------------------- """


cdef extern from "cpp/kinematics/tensor_algebra.cpp":
  pass

""" ----------------------------------------------------------------------------
End of Source Files
---------------------------------------------------------------------------- """


# ------------------------------------------------------------------------------
# C++ Header files + exported definitions
# ------------------------------------------------------------------------------

cdef extern from "cpp/kinematics/tensor_algebra.hpp" namespace "constitutive_models":
  cdef double ddot(double[] a, double[] b)

  cdef void addto(double[] a, double[] b, int dim)

