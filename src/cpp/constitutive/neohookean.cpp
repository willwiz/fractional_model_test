#include <cmath>
#include "../kinematics/tensor_algebra.hpp"
#include "../kinematics/kinematics.hpp"
#include "neohookean.hpp"

namespace constitutive_models {

/*----------------------------------------------------------------------
 |  Standard Neohookean, no much to say
 |
 |  Author: Will Zhang
 |  Dependencies: None
 -----------------------------------------------------------------------*/

  NeoHookean::NeoHookean(double mu)
  {
    this->set_pars(mu);
  }

  void NeoHookean::set_pars(double mu) {

    this -> mu = mu;
  }

  double NeoHookean::stress(const kinematics::kinematics<4> &kin, double stress[]){

    for (int i = 0; i < 4; i++)
    {
      stress[i] = mu*id2d[i];
    }
    return mu;
  }

  void NeoHookean::stress(double args[], double stress[]){

    kinematics::deformation2D kin(args);
    double p = this->stress(kin, stress);
    for (int i = 0; i < 4; i++)
    {
      stress[i] = stress[i] - p*kin.I_n*kin.Cinv[i];
    }
  }

  NeoHookean3D::NeoHookean3D(double mu)
  {
    this->set_pars(mu);
  }

  void NeoHookean3D::set_pars(double mu) {

    this -> mu = mu;
  }

  double NeoHookean3D::stress(const kinematics::kinematics<9> &kin, double stress[]){

    for (int i = 0; i < 9; i++)
    {
      stress[i] = 0.0;
    }

    for (int i = 0; i < 3; i++)
    {
      stress[4*i] = mu;
    }

    return mu;
  }

  void NeoHookean3D::stress(double args[], double stress[]){

    kinematics::deformation3D kin(args);
    double p = this->stress(kin, stress);
    for (int i = 0; i < 4; i++)
    {
      stress[i] = stress[i] - p*kin.I_n*kin.Cinv[i];
    }
  }



}
