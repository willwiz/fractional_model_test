# File: kinematics.pxd
# distutils: language = c++
# cython: language_level=3


""" ----------------------------------------------------------------------------
C++ Source Files
---------------------------------------------------------------------------- """


cdef extern from "cpp/kinematics/kinematics.cpp":
  pass

""" ----------------------------------------------------------------------------
End of Source Files
---------------------------------------------------------------------------- """


# ------------------------------------------------------------------------------
# C++ Header files + exported definitions
# ------------------------------------------------------------------------------

cdef extern from "cpp/kinematics/kinematics.hpp" namespace "kinematics":
  cdef cppclass kinematics2D:
    double det
    double I_n
    double I_1
    double I_1m3
    double C[4]
    double Cinv[4]
    kinematics2D() except +

  cdef cppclass deformation2D:
    deformation2D() except +
    deformation2D(double[] vC) except +
    void precompute(double[] vC)

  cdef cppclass deformation_ensemble2D:
    deformation_ensemble2D() except +
    deformation_ensemble2D(double eb_strain) except +
    void precompute(double eb_strain)

