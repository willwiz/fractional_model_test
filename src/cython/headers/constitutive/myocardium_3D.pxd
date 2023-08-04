# File: myocardium_3D.pxd
# distutils: language = c++
# cython: language_level=3


""" ----------------------------------------------------------------------------
C++ Source Files
---------------------------------------------------------------------------- """

cimport src.cython.headers.kinematics.tensor_algebra
cimport src.cython.headers.kinematics.kinematics
cimport src.cython.headers.constitutive.interfaces

cdef extern from "src/cpp/constitutive/myocardium_3D.cpp":
  pass

""" ----------------------------------------------------------------------------
End of Source Files
---------------------------------------------------------------------------- """


# ------------------------------------------------------------------------------
# C++ Header files + exported definitions
# ------------------------------------------------------------------------------

cdef extern from "src/cpp/constitutive/myocardium_3D.hpp" namespace "constitutive_models":
  cdef cppclass Myocardium:
    double mxm[9]
    double nxn[9]
    double zxz[9]
    double mxn[9]
    double mxz[9]
    double nxz[9]
    Myocardium() except +
    Myocardium(double b1, double b2, double kff, double kss, double knn,
      double kfs, double kfn, double ksn, double[] fiber) except +
    void set_pars(double b1, double b2, double kff, double kss, double knn,
      double kfs, double kfn, double ksn, double[] fiber)
    void stress(double[] args, double[] stress)

