#pragma once

#include "../kinematics/kinematics.hpp"

namespace constitutive_models
{

  class MatLawInterface
  {
  public:
    virtual double stress(const kinematics::kinematics2D &kin, double stress[]) = 0;
    virtual void stress(double args[], double stress[]) = 0;
  };


  class MatLawTimeInterface
  {
  public:
    virtual void stress(const kinematics::kinematics2D &kin, const double dt, double stress[]) = 0;
  };


} // namespace constitutive_models
