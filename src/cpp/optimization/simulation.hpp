#pragma once

namespace sim {

  void femoral_get_model_parameters(double pars[], double fiber[], double visco[], double Tf,
    double pars_out[11]);

  void femoral_get_model_parameters_scaled(double pars[], double fiber[], double visco[], double Tf,
    double Cmax[], double pars_out[11]);

  void thoracic_default_get_model_parameters_scaled(double pars[], double fiber[], double visco[], double Tf,
    double Cmax[], double pars_out[]);

  void planar_elastin_matrix_simulate(
    double pars[], double fiber[], double caputo[],
    double Tf, double Cmax[], double args[], double dt[], double stress[], int n
  );

  void femoral_he_simulate(double pars[], double fiber[], double caputo[],
    double Tf, double Cmax[], double args[], double dt[], double stress[], int n);

  void femoral_ve_simulate(double pars[], double fiber[], double caputo[],
    double Tf, double Cmax[], double args[], double dt[], double stress[], int n);

  void thoracic_default_ve_simulate_scaled(double pars[], double fiber[], double caputo[],
    double Tf, double Cmax[], double args[], double dt[], double stress[], int n);

  void myocardium_vs_simulation(double pars[], double fiber[], double caputo[],
    double Tf, double args[], double dt[], double stress[], int n);

}