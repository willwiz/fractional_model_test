# File: simulation.pxd
# distutils: language = c++
# cython: language_level=3


""" ----------------------------------------------------------------------------
C++ Source Files
---------------------------------------------------------------------------- """

cimport src.cython.headers.optimization.templates
cimport src.cython.headers.tissue_models.models

cdef extern from "src/cpp/optimization/simulation.cpp":
  pass

""" ----------------------------------------------------------------------------
End of Source Files
---------------------------------------------------------------------------- """


# ------------------------------------------------------------------------------
# C++ Header files + exported definitions
# ------------------------------------------------------------------------------

cdef extern from "src/cpp/optimization/simulation.hpp" namespace "sim":
  cdef void femoral_get_model_parameters(double[] pars, double[] fiber,
    double[] visco, double Tf, double[] pars_out)

  cdef void femoral_get_model_parameters_scaled(double[] pars, double[] fiber,
    double[] visco, double Tf, double[] Cmax, double[] pars_out)

  cdef void thoracic_default_get_model_parameters_scaled(double[] pars,
    double[] fiber, double[] visco, double Tf, double[] Cmax, double[] pars_out)

  cdef void planar_elastin_matrix_simulate(double[] pars, double[] fiber,
    double[] caputo, double Tf, double[] Cmax, double[] args, double[] dt,
    double[] stress, int n)

  cdef void femoral_he_simulate(double[] pars, double[] fiber, double[] caputo,
    double Tf, double[] Cmax, double[] args, double[] dt, double[] stress,
    int n)

  cdef void femoral_ve_simulate(double[] pars, double[] fiber, double[] caputo,
    double Tf, double[] Cmax, double[] args, double[] dt, double[] stress,
    int n)

  cdef void thoracic_default_ve_simulate_scaled(double[] pars, double[] fiber,
    double[] caputo, double Tf, double[] Cmax, double[] args, double[] dt,
    double[] stress, int n)

  cdef void myocardium_vs_simulation(double[] pars, double[] fiber,
    double[] caputo, double Tf, double[] args, double[] dt, double[] stress,
    int n)

