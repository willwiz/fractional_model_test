#pragma once

#include "caputo.hpp"
#include "../kinematics/kinematics.hpp"
#include "../constitutive/interfaces.hpp"


namespace constitutive_models
{
  template<int dim>
  class FractionalVE
  {
  private:
    caputo::caputo_init_vec<dim> store;
    caputo::caputo_init_scl store_p;
  public:
    MatLawInterface<dim> *m_law;

    FractionalVE(MatLawInterface<dim> &law, const double alpha, const double Tf);

    ~FractionalVE() {}

    double stress(const kinematics::kinematics<dim> &kin, const double dt, double stress[]);
    void stress(const double args[], const double dt, double stress[]);
  };

}
