# File: planar_hog.pxd
# distutils: language = c++
# cython: language_level=3


""" ----------------------------------------------------------------------------
C++ Source Files
---------------------------------------------------------------------------- """

cimport cython.headers.kinematics.kinematics
cimport cython.headers.kinematics.tensor_algebra
cimport cython.headers.constitutive.interfaces

cdef extern from "cpp/constitutive/planar_hog.cpp":
  pass

""" ----------------------------------------------------------------------------
End of Source Files
---------------------------------------------------------------------------- """


# ------------------------------------------------------------------------------
# C++ Header files + exported definitions
# ------------------------------------------------------------------------------

cdef extern from "cpp/constitutive/planar_hog.hpp" namespace "constitutive_models":
  cdef cppclass PlanarHog2D:
    double k1
    double k2
    double m[4]
    double E1
    double E2
    PlanarHog2D() except +
    PlanarHog2D(double k1, double k2, double theta, double kappa) except +
    PlanarHog2D(double k1, double k2, double theta, double kappa, double[] Cmax) except +
    void set_pars(double theta, double kappa)
    void set_pars(double theta, double kappa, double[] Cmax)
    double get_scaled_modulus()
    void stress(double[] args, double[] stress)

