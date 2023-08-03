# File: interfaces.pxd
# distutils: language = c++
# cython: language_level=3


""" ----------------------------------------------------------------------------
C++ Source Files
---------------------------------------------------------------------------- """

cimport cython.headers.kinematics.kinematics


""" ----------------------------------------------------------------------------
End of Source Files
---------------------------------------------------------------------------- """


# ------------------------------------------------------------------------------
# C++ Header files + exported definitions
# ------------------------------------------------------------------------------

cdef extern from "cpp/constitutive/interfaces.hpp" namespace "constitutive_models":
  cdef cppclass MatLawInterface:
    pass

  cdef cppclass MatLawTimeInterface:
    pass

