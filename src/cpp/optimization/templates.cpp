#include <cmath>
#include <algorithm>
#include "../CTvalues_optimization.hpp"
#include "templates.hpp"

namespace residuals {


/* ------------------------------------------------------------------------------
 |  This file provides the definitions for calculating the residuals for
 |  the different model forms
 |
 |  These models are mainly used for the collaboration with Alexey Kamenskiy
 |
 |  Author: Will Zhang
 |  Dependencies: None
 ----------------------------------------------------------------------------- */


  template<class matlaw>
  void simulate(double pars[], double fiber[], double caputo[],
    double Tf, double Cmax[], double args[], double dt[], double stress[], int n)
  {
    int strd_i;

    double vals[4];

    kinematics::deformation2D kin;
    matlaw law(pars, fiber, caputo, Tf, Cmax);

    for (int i = 1; i < n; i++)
    {
      strd_i = 4 * i;
      // Calculate deformation
      kin.precompute(&args[strd_i]);
      // Compute Final Stress
      law.stress(kin, dt[i], vals);
      for (int j = 0; j < 4; j++)
      {
        stress[strd_i + j] = vals[j];
      }
    }
  }

  template<class matlaw>
  void simulate3D(double pars[], double fiber[], double caputo[],
    double Tf, double Cmax[], double args[], double dt[], double stress[], int n)
  {
    int strd_i;

    double vals[9];

    kinematics::deformation3D kin;
    matlaw law(pars, fiber, caputo, Tf, Cmax);

    for (int i = 1; i < n; i++)
    {
      strd_i = 9 * i;
      // Calculate deformation
      kin.precompute(&args[strd_i]);
      // Compute Final Stress
      law.stress(kin, dt[i], vals);
      for (int j = 0; j < 9; j++)
      {
        stress[strd_i + j] = vals[j];
      }
    }
  }


  template<SimulateFunction simfunc, ResidualCalculation resfunc>
  double calc_residual_general(
    double pars[], double fiber[], double visco[], double Tf, double Cmax[],
    double args[], double stress[], double dt[], double weights[],
    double deltaCG[], double hysteresis[], double alphas[],
    int index[], int select[], int n, int dim, int nprot, int skip)
  {
    double * sims = new double[n*dim]();

    simfunc(pars, fiber, visco, Tf, Cmax, args, dt, &sims[0], n);

    double res = resfunc(args, stress, weights, index, select, dim, nprot, skip, sims);

    delete [] sims;

    return res;
  }


/* ******************************************************************************
 * Basic functions, e.g. calculating the residual, penalty, hysteresis etc.
 *
 * COMMENTS:
 * This is the same for all of the models, so they share these same codes
****************************************************************************** */
  // Residual Calculation


  inline double quadratic_residual(double sim, double data){
      double difference = sim - data;
      return difference * difference;
  }

  double residual_body(double strain[], double stress[], double weights[],
    int index[], int select[], int dim, int nprot, int skip,
    double sims[])
  {

    int strd_i, strd_k;
    double res, eps;
    int kid, start, stop;

    res = 0;
    for (int k = 0; k < nprot; k++)
    {
      kid    = select[k];
      strd_k = dim*kid;
      start  = index[kid];
      stop   = index[kid + 1] + 1;
      for (int j = 0; j < dim; j+=3)
      {
        eps = 0;

        for (int i = start; i < stop; i+=skip)
        {
          strd_i = i*dim + j;
          eps = eps + quadratic_residual(sims[strd_i], stress[strd_i]);

        }

        res = res + weights[strd_k + j] * eps;

      }
    }
    return res;
  }


/*------------------------------------------------------------------------------
 |  THE END
 -----------------------------------------------------------------------------*/
}

