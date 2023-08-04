# File: kinematics.pxd
# distutils: language = c++
# cython: language_level=3


""" ----------------------------------------------------------------------------
C++ Source Files
---------------------------------------------------------------------------- """


cdef extern from "src/cpp/kinematics/kinematics.cpp":
  pass

""" ----------------------------------------------------------------------------
End of Source Files
---------------------------------------------------------------------------- """


# ------------------------------------------------------------------------------
# C++ Header files + exported definitions
# ------------------------------------------------------------------------------

cdef extern from "src/cpp/kinematics/kinematics.hpp" namespace "kinematics":
  cdef cppclass deformation2D:
    deformation2D() except +
    deformation2D(double[] vC) except +
    void precompute(double[] vC)

  cdef cppclass deformation_ensemble2D:
    deformation_ensemble2D() except +
    deformation_ensemble2D(double eb_strain) except +
    void precompute(double eb_strain)

  cdef cppclass deformation3D:
    deformation3D() except +
    deformation3D(double[] vC) except +
    void precompute(double[] vC)

