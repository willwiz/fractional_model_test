# File: caputo.pxd
# distutils: language = c++
# cython: language_level=3


""" ----------------------------------------------------------------------------
C++ Source Files
---------------------------------------------------------------------------- """


cdef extern from "src/cpp/fractional/caputo.cpp":
  pass

""" ----------------------------------------------------------------------------
End of Source Files
---------------------------------------------------------------------------- """


# ------------------------------------------------------------------------------
# C++ Header files + exported definitions
# ------------------------------------------------------------------------------

cdef extern from "src/cpp/fractional/caputo.hpp" namespace "caputo":
  cdef cppclass caputo_init:
    double alpha
    double Tf
    double delta
    double betas[9]
    double taus[9]
    double beta0
    caputo_init() except +
    caputo_init(double alpha, double Tf, double delta) except +
    void set_pars(double alpha, double Tf, double delta)
    void update_dt(double dt)
    void update_dt_lin(double dt)

  cdef cppclass caputo_init_scl:
    double Q[9]
    double df
    double f_prev
    caputo_init_scl() except +
    caputo_init_scl(double alpha, double Tf, double delta) except +
    double caputo_iter(double fn, double dt)
    double diffeq_iter(double fn, double dt)

  cdef double interpolate1D_newton_linear(double p1, double p2, double t)

  cdef double extrapolate1D_newton_linear(double p1, double p2, double t)

  cdef double interpolate_caputo_parameter_arr(double alpha, double[] arr)

  cdef double interpolate_caputo_parameter_beta(double alpha, double[] arr)

  cdef double interpolate_caputo_parameter_taus(double alpha, double[] arr)

