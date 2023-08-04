# File: hog_2D.pxd
# distutils: language = c++
# cython: language_level=3


""" ----------------------------------------------------------------------------
C++ Source Files
---------------------------------------------------------------------------- """

cimport src.cython.headers.kinematics.tensor_algebra
cimport src.cython.headers.kinematics.kinematics
cimport src.cython.headers.constitutive.interfaces

cdef extern from "src/cpp/constitutive/hog_2D.cpp":
  pass

""" ----------------------------------------------------------------------------
End of Source Files
---------------------------------------------------------------------------- """


# ------------------------------------------------------------------------------
# C++ Header files + exported definitions
# ------------------------------------------------------------------------------

cdef extern from "src/cpp/constitutive/hog_2D.hpp" namespace "constitutive_models":
  cdef cppclass Hog2D:
    double k1
    double k2
    double m[4]
    double E1
    double E2
    Hog2D() except +
    Hog2D(double k1, double k2, double theta) except +
    Hog2D(double k1, double k2, double theta, double[] Cmax) except +
    void set_pars(double k1, double k2, double theta)
    void set_pars(double k1, double k2, double theta, double[] Cmax)
    double get_scaled_modulus()
    void stress(double[] args, double[] stress)

