# File: neohookean.pxd
# distutils: language = c++
# cython: language_level=3


""" ----------------------------------------------------------------------------
C++ Source Files
---------------------------------------------------------------------------- """

cimport src.cython.headers.kinematics.tensor_algebra
cimport src.cython.headers.kinematics.kinematics
cimport src.cython.headers.constitutive.interfaces

cdef extern from "src/cpp/constitutive/neohookean.cpp":
  pass

""" ----------------------------------------------------------------------------
End of Source Files
---------------------------------------------------------------------------- """


# ------------------------------------------------------------------------------
# C++ Header files + exported definitions
# ------------------------------------------------------------------------------

cdef extern from "src/cpp/constitutive/neohookean.hpp" namespace "constitutive_models":
  cdef cppclass NeoHookean:
    double mu
    NeoHookean() except +
    NeoHookean(double mu) except +
    void set_pars(double mu)
    void stress(double[] args, double[] stress)

  cdef cppclass NeoHookean3D:
    double mu
    NeoHookean3D() except +
    NeoHookean3D(double mu) except +
    void set_pars(double mu)
    void stress(double[] args, double[] stress)

