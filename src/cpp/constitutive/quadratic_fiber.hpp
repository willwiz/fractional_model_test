#pragma once

#include "../kinematics/kinematics.hpp"
#include "interfaces.hpp"

namespace constitutive_models
{
  class QuadraticFiber: public MatLawInterface
  {

  public:
    double k;
    double m4[4];
    double m6[4];
    QuadraticFiber();
    ~QuadraticFiber();
    QuadraticFiber(double mu, double theta, double alpha, double beta);

    void set_pars(double mu, double theta, double alpha, double beta);
    double stress(const kinematics::kinematics2D &kin, double stress[4]);
    void stress(double args[4], double stress[4]);
  };

} // namespace constitutive_models
