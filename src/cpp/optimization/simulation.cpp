#include "../tissue_models/models.hpp"
#include "templates.hpp"
#include "simulation.hpp"

/*----------------------------------------------------------------------
 |  This file provides the definitions of the different model forms
 |  which combines the primative constitive model from the other cpp files
 |  in the constitutive_models namespace
 |
 |  These models are mainly used for the collaboration with Alexey Kamenskiy
 |
 |  Author: Will Zhang
 |  Dependencies: None
 -----------------------------------------------------------------------*/


using namespace constitutive_models;

namespace sim {


/*----------------------------------------------------------------------
 |  This provides the main models in the full constitutive model
 -----------------------------------------------------------------------*/

  void femoral_get_model_parameters(double pars[], double fiber[], double visco[], double Tf,
    double pars_out[11])
  {
    Femoral psi(pars, fiber);
    psi.get_scaled_pars(&pars_out[0]);
    pars_out[7]  = fiber[0];
    pars_out[8]  = fiber[1];
    pars_out[9]  = visco[0];
    pars_out[10] = visco[1];
  }

  void femoral_get_model_parameters_scaled(double pars[], double fiber[], double visco[], double Tf,
    double Cmax[], double pars_out[11])
  {
    Femoral psi(pars, fiber);
    psi.get_scaled_pars(&pars_out[0]);
    pars_out[7]  = fiber[0];
    pars_out[8]  = fiber[1];
    pars_out[9]  = visco[0];
    pars_out[10] = visco[1];
  }



  void thoracic_default_get_model_parameters_scaled(double pars[], double fiber[], double visco[], double Tf,
    double Cmax[], double pars_out[])
  {
    ThoracicDefaultBase psi(pars, fiber, Cmax);
    psi.get_scaled_pars(&pars_out[0]);
    pars_out[4] = fiber[0];
    pars_out[5] = fiber[1];
    pars_out[6] = visco[0];
  }


  /*----------------------------------------------------------------------
  |  Some basic models
  -----------------------------------------------------------------------*/

  void planar_elastin_matrix_simulate(
    double pars[], double fiber[], double caputo[],
    double Tf, double Cmax[], double args[], double dt[], double stress[], int n
  ) {
    residuals::simulate<PlanarElastinMatrix>(pars, fiber, caputo, Tf, Cmax, args, dt, stress, n);
  }

  void thoracic_default_ve_simulate_scaled(double pars[], double fiber[], double caputo[], double Tf, double Cmax[],
    double args[], double dt[], double stress[], int n)
  {
    residuals::simulate<ThoracicDefaultVEScaled>(pars, fiber, caputo, Tf, Cmax, args, dt, stress, n);
  }

  /*----------------------------------------------------------------------
  |  The femoral artery models
  -----------------------------------------------------------------------*/

  void femoral_he_simulate(double pars[], double fiber[], double caputo[],
    double Tf, double Cmax[], double args[], double dt[], double stress[], int n)
  {
    residuals::simulate<Femoral>(pars, fiber, caputo, Tf, Cmax, args, dt, stress, n);
  }


  void femoral_ve_simulate(double pars[], double fiber[], double caputo[],
    double Tf, double Cmax[], double args[], double dt[], double stress[], int n)
  {
    residuals::simulate<FemoralVE>(pars, fiber, caputo, Tf, Cmax, args, dt, stress, n);
  }


  void myocardium_vs_simulation(double pars[], double fiber[], double caputo[],
    double Tf, double Cmax[], double args[], double dt[], double stress[], int n)
  {
    residuals::simulate3D<MyocardiumVE>(pars, fiber, caputo, Tf, Cmax, args, dt, stress, n);
  }

}