# File: quadratic_fiber.pxd
# distutils: language = c++
# cython: language_level=3


""" ----------------------------------------------------------------------------
C++ Source Files
---------------------------------------------------------------------------- """

cimport src.cython.headers.kinematics.tensor_algebra
cimport src.cython.headers.kinematics.kinematics
cimport src.cython.headers.constitutive.interfaces

cdef extern from "src/cpp/constitutive/quadratic_fiber.cpp":
  pass

""" ----------------------------------------------------------------------------
End of Source Files
---------------------------------------------------------------------------- """


# ------------------------------------------------------------------------------
# C++ Header files + exported definitions
# ------------------------------------------------------------------------------

cdef extern from "src/cpp/constitutive/quadratic_fiber.hpp" namespace "constitutive_models":
  cdef cppclass QuadraticFiber:
    double k
    double m4[4]
    double m6[4]
    QuadraticFiber() except +
    QuadraticFiber(double mu, double theta, double alpha, double beta) except +
    void set_pars(double mu, double theta, double alpha, double beta)
    void stress(double[] args, double[] stress)

