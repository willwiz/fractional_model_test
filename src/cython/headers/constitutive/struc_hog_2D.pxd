# File: struc_hog_2D.pxd
# distutils: language = c++
# cython: language_level=3


""" ----------------------------------------------------------------------------
C++ Source Files
---------------------------------------------------------------------------- """

cimport cython.headers.kinematics.kinematics
cimport cython.headers.kinematics.tensor_algebra
cimport cython.headers.constitutive.interfaces

cdef extern from "cpp/constitutive/struc_hog_2D.cpp":
  pass

""" ----------------------------------------------------------------------------
End of Source Files
---------------------------------------------------------------------------- """


# ------------------------------------------------------------------------------
# C++ Header files + exported definitions
# ------------------------------------------------------------------------------

cdef extern from "cpp/constitutive/struc_hog_2D.hpp" namespace "constitutive_models":
  cdef cppclass StrucHOG2D:
    double k1
    double k2
    double A
    double B
    double C
    double m4[4]
    double m6[4]
    double H4[4]
    double H6[4]
    double E1
    double E2
    StrucHOG2D() except +
    StrucHOG2D(double k1, double k2, double theta, double alpha, double beta,
      double kip, double kop) except +
    StrucHOG2D(double k1, double k2, double theta, double alpha, double beta,
      double kip, double kop, double[] Cmax) except +
    void set_pars(double k1, double k2, double theta, double alpha, double beta,
      double kip, double kop)
    void set_pars(double k1, double k2, double theta, double alpha, double beta,
      double kip, double kop, double[] Cmax)
    double get_scaled_modulus()
    void stress(double[] args, double[] stress)

