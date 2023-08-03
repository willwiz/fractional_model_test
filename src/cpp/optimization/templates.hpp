#pragma once

#include "../constitutive/interfaces.hpp"

namespace residuals {

  typedef double (*ResidualCalculation) (double*, double*, double*, int*, int*, int, int, int, double*);


  template<class matlaw>
  void simulate(double pars[], double fiber[], double caputo[],
    double Tf, double Cmax[], double args[], double dt[], double stress[], int n);


  template<class matlaw, ResidualCalculation resfunc>
  double calc_residual_general(
    double pars[], double fiber[], double visco[], double Tf, double Cmax[],
    double args[], double stress[], double dt[], double weights[],
    double deltaCG[], double hysteresis[], double alphas[],
    int index[], int select[], int n, int dim, int nprot, int skip);


  double residual_body(double strain[], double stress[], double weights[],
    int index[], int select[], int dim, int nprot, int skip,
    double sims[]);


  // Residual templates

  template<class matlaw>
  double calc_residual(double pars[], double fiber[],
    double visco[], double Tf, double Cmax[],
    double args[], double stress[], double dt[], double weights[],
    double deltaCG[], double hysteresis[], double alphas[],
    int index[], int select[], int n, int dim, int nprot, int skip);

}