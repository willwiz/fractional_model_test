# File: fractional.pxd
# distutils: language = c++
# cython: language_level=3


""" ----------------------------------------------------------------------------
C++ Source Files
---------------------------------------------------------------------------- """

cimport src.cython.headers.kinematics.kinematics
cimport src.cython.headers.constitutive.interfaces
cimport src.cython.headers.fractional.caputo

cdef extern from "src/cpp/fractional/fractional.cpp":
  pass

""" ----------------------------------------------------------------------------
End of Source Files
---------------------------------------------------------------------------- """


# ------------------------------------------------------------------------------
# C++ Header files + exported definitions
# ------------------------------------------------------------------------------

cdef extern from "src/cpp/fractional/fractional.hpp" namespace "constitutive_models":

  pass