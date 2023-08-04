#pragma once

#include "../kinematics/kinematics.hpp"

namespace constitutive_models
{

  template<int dim>
  class MatLawInterface
  {
  public:
    virtual double stress(const kinematics::kinematics<dim> &kin, double stress[dim]) = 0;
    virtual void stress(double args[dim], double stress[dim]) = 0;
  };

  template<int dim>
  class MatLawTimeInterface
  {
  public:
    virtual void stress(const kinematics::kinematics<dim> &kin, const double dt, double stress[]) = 0;
  };


} // namespace constitutive_models
