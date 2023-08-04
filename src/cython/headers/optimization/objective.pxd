# File: objective.pxd
# distutils: language = c++
# cython: language_level=3


""" ----------------------------------------------------------------------------
C++ Source Files
---------------------------------------------------------------------------- """

cimport src.cython.headers.optimization.templates
cimport src.cython.headers.tissue_models.models

cdef extern from "src/cpp/optimization/objective.cpp":
  pass

""" ----------------------------------------------------------------------------
End of Source Files
---------------------------------------------------------------------------- """


# ------------------------------------------------------------------------------
# C++ Header files + exported definitions
# ------------------------------------------------------------------------------

cdef extern from "src/cpp/optimization/objective.hpp" namespace "residuals":
  cdef double planar_elastin_matrix_residual(double[] pars, double[] fiber,
    double[] visco, double Tf, double[] Cmax, double[] args, double[] stress,
    double[] dt, double[] weights, double[] deltaCG, double[] hysteresis,
    double[] alphas, int[] index, int[] select, int n, int dim, int nprot,
    int skip)

  cdef double femoral_residual_HE(double[] pars, double[] fiber, double[] visco,
    double Tf, double[] Cmax, double[] args, double[] stress, double[] dt,
    double[] weights, double[] deltaCG, double[] hysteresis, double[] alphas,
    int[] index, int[] select, int n, int dim, int nprot, int skip)

  cdef double femoral_residual_VE(double[] pars, double[] fiber, double[] visco,
    double Tf, double[] Cmax, double[] args, double[] stress, double[] dt,
    double[] weights, double[] deltaCG, double[] hysteresis, double[] alphas,
    int[] index, int[] select, int n, int dim, int nprot, int skip)

  cdef double thoracic_default_residual_VE_scaled_hyst_relax(double[] pars,
    double[] fiber, double[] visco, double Tf, double[] Cmax, double[] args,
    double[] stress, double[] dt, double[] weights, double[] deltaCG,
    double[] hysteresis, double[] alphas, int[] index, int[] select, int n,
    int dim, int nprot, int skip)

